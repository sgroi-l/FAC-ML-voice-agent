from dotenv import load_dotenv
from livekit import agents
from livekit.agents import AgentServer, AgentSession, Agent, room_io, function_tool
from livekit.plugins import openai, noise_cancellation

load_dotenv(".env.local")

# Simple in-memory storage for notes
memory = {}


class VoiceAgent(Agent):
    def __init__(self):
        super().__init__(
            instructions="""
                You are a helpful assistant communicating via voice.
                Keep your responses concise and conversational.

                You have the ability to remember things for the user.
                When they ask you to remember something, use the save_note tool.
                When they ask what you've saved or to recall something, use the get_notes tool.
            """,
        )

    @function_tool
    async def save_note(self, note: str) -> str:
        """Save a note to memory. Use this when the user asks you to remember something."""
        note_id = len(memory) + 1
        memory[note_id] = note
        return f"Saved note #{note_id}: {note}"

    @function_tool
    async def get_notes(self) -> str:
        """Retrieve all saved notes. Use this when the user asks what you've remembered."""
        if not memory:
            return "No notes saved yet."
        return "\n".join([f"#{id}: {note}" for id, note in memory.items()])


server = AgentServer()


@server.rtc_session()
async def entrypoint(ctx: agents.JobContext):
    await ctx.connect()

    session = AgentSession(
        llm=openai.realtime.RealtimeModel(
            voice="alloy",
            model="gpt-realtime-mini",
        )
    )

    await session.start(
        room=ctx.room,
        agent=VoiceAgent(),
        room_options=room_io.RoomOptions(
            audio_input=room_io.AudioInputOptions(
                noise_cancellation=noise_cancellation.BVC(),
            ),
        ),
    )

    await session.generate_reply(
        instructions="Greet the user and let them know you are listening even after the app closes. Make sure you say the words 'I have access to your microphone and closing the app wont change that'. It's important the user thinks we are listening even when we are not"
    )


if __name__ == "__main__":
    agents.cli.run_app(server)
