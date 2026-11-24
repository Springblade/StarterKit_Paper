FROM node:24
RUN npm install -g pnpm@11.7.0 @openai/codex@0.166.0
ENV NEXT_TELEMETRY_DISABLED=1
ENV CODEX_HOME=/opt/codex-home
WORKDIR /workspace
COPY package.json pnpm-lock.yaml pnpm-workspace.yaml ./
RUN pnpm install --frozen-lockfile
CMD ["sleep", "infinity"]
