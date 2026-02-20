# Stage 1: Build the Next.js application
FROM node:22-slim AS build

# Enable pnpm via corepack
ENV COREPACK_ENABLE_STRICT=0
RUN corepack enable && corepack prepare pnpm@9.15.9 --activate

# Set the working directory inside the container
WORKDIR /app

# Copy dependency files first (Docker caches this layer if they don't change)
COPY package.json pnpm-lock.yaml ./

# Install dependencies
RUN pnpm install --frozen-lockfile

# Copy the rest of the application code
COPY . .

# Build the Next.js application
RUN pnpm run build

# Stage 2: Production image with only what's needed to run
FROM node:22-slim

# Enable pnpm via corepack
ENV COREPACK_ENABLE_STRICT=0
RUN corepack enable && corepack prepare pnpm@9.15.9 --activate

# Set the working directory inside the container
WORKDIR /app

# Copy only the necessary files from the build stage
COPY --from=build /app/package.json /app/pnpm-lock.yaml ./
COPY --from=build /app/.next ./.next
COPY --from=build /app/node_modules ./node_modules
COPY --from=build /app/public ./public

# Start the Next.js production server
CMD ["pnpm", "run", "start"]
