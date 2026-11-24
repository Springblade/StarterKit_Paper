FROM smartkit-pilot:20261111
# Common, pinned browser infrastructure; application dependencies/logic unchanged.
RUN mkdir -p /opt/behavior && cd /opt/behavior && npm init -y >/dev/null && npm install --save-exact playwright@1.58.2
RUN /opt/behavior/node_modules/.bin/playwright install --with-deps chromium
ENV PATH="/opt/behavior/node_modules/.bin:${PATH}"
ENV NEXT_TELEMETRY_DISABLED=1
