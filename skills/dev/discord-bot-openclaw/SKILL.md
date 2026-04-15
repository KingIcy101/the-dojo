---
name: discord-bot-openclaw
description: Multi-agent Discord bot with per-agent webhook channels, slash commands, and PM2 management using discord.js v14.
category: dev
---

# Discord Bot (OpenClaw Multi-Agent)

## When to Use
Setting up or modifying the Discord bot that serves as the communication layer for the OpenClaw agent team.

## Architecture
One bot token, multiple agents posting via per-agent Discord webhooks. Bot handles slash commands and incoming events; agents post updates to their dedicated channels via webhooks (no bot token needed for posting).

## Key Config

```
Guild ID: configure in .env as DISCORD_GUILD_ID
Bot Token: DISCORD_BOT_TOKEN in voice-server/.env
Channel IDs:
  dev-team-chat:    1484725229723844758
  agency-team-chat: 1485787941379903559
```

## Steps

1. Create bot at discord.com/developers → copy token
2. Add to server with `bot` + `applications.commands` scopes
3. Set env vars: `DISCORD_BOT_TOKEN`, `DISCORD_GUILD_ID`
4. Register slash commands on startup
5. Create webhook per agent channel → store webhook URLs in .env
6. Agents post via webhook URL (no bot token needed)
7. Manage bot process via PM2

## Key Patterns / Code

### Bot Setup (discord.js v14)
```js
const { Client, GatewayIntentBits, REST, Routes } = require('discord.js');

const client = new Client({
  intents: [GatewayIntentBits.Guilds, GatewayIntentBits.GuildMessages, GatewayIntentBits.MessageContent],
});

client.once('ready', () => console.log(`Bot ready: ${client.user.tag}`));

client.on('interactionCreate', async (interaction) => {
  if (!interaction.isChatInputCommand()) return;
  if (interaction.commandName === 'status') {
    await interaction.reply('All systems operational.');
  }
});

client.login(process.env.DISCORD_BOT_TOKEN);
```

### Register Slash Commands
```js
const commands = [{ name: 'status', description: 'Check agent status' }];
const rest = new REST().setToken(process.env.DISCORD_BOT_TOKEN);

await rest.put(
  Routes.applicationGuildCommands(CLIENT_ID, GUILD_ID),
  { body: commands }
);
```

### Agent Webhook Posting (no bot token)
```js
async function postToDiscord(webhookUrl, agentName, message) {
  await fetch(webhookUrl, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({
      username: agentName,       // shows as agent name
      avatar_url: AGENT_AVATAR,  // agent avatar URL
      content: message,
    }),
  });
}
```

### PM2 Management
```bash
pm2 restart discord-bot
pm2 logs discord-bot --lines 50
pm2 show discord-bot
```

## Gotchas
- Slash commands take up to 1 hour to propagate globally — use guild commands for instant update during dev
- `MessageContent` intent requires enabling in Discord Developer Portal under "Privileged Gateway Intents"
- Webhook URL = agent's posting mechanism — keep separate from bot token
- Each agent should have its own webhook URL for its channel (create in channel settings)
- Avatar generation: use consistent 512x512 portrait per agent, upload to a stable URL
- discord.js v14 requires Node 16.11.0+ — check `node -v` before install
