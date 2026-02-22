module.exports = {
  apps: [
    {
      name: 'mission-control',
      script: 'server.js',
      cwd: '/Users/mattbender/.openclaw/workspace/mission-control-server',
      env: {
        NODE_ENV: 'production',
        MC_PORT: 7900,
        WORKSPACE: '/Users/mattbender/.openclaw/workspace',
      },
      restart_delay: 3000,
      max_restarts: 10,
    },
    {
      name: 'mc-tunnel',
      script: '/Users/mattbender/bin/cloudflared',
      args: 'tunnel --url http://localhost:7900 --no-autoupdate',
      autorestart: true,
      restart_delay: 5000,
      max_restarts: 20,
      log_file: '/Users/mattbender/.openclaw/workspace/mission-control-server/tunnel.log',
    },
  ],
};
