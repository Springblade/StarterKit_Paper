FROM node:24.22.2-bookworm
RUN npm install -g pnpm@11.7.0
ENV NEXT_TELEMETRY_DISABLED=1
WORKDIR /workspace
COPY package.json pnpm-lock.yaml pnpm-workspace.yaml ./
RUN pnpm install --frozen-lockfile
RUN mkdir -p /opt/behavior && cd /opt/behavior && npm init -y >/dev/null && npm install --save-exact playwright@1.58.2
RUN /opt/behavior/node_modules/.bin/playwright install --with-deps chromium
CMD ["sleep", "infinity"]
