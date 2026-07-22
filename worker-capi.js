/**
 * Nottingville — Meta Conversions API (CAPI) Cloudflare Worker
 *
 * Deploy: npx wrangler deploy worker-capi.js --name nottingville-capi
 * Set secrets:
 *   npx wrangler secret put META_ACCESS_TOKEN
 *
 * Then set window.__CAPI_ENDPOINT in index.html to your worker URL:
 *   https://nottingville-capi.<your-subdomain>.workers.dev/event
 */

const PIXEL_ID = '558125623033328';
const API_VERSION = 'v21.0';

export default {
  async fetch(request, env) {
    // CORS preflight
    if (request.method === 'OPTIONS') {
      return new Response(null, {
        headers: corsHeaders('https://nottingville.space'),
      });
    }

    if (request.method !== 'POST') {
      return new Response('Method not allowed', { status: 405 });
    }

    const url = new URL(request.url);
    if (url.pathname !== '/event') {
      return new Response('Not found', { status: 404 });
    }

    try {
      const body = await request.json();
      const {
        event_name,
        event_id,
        event_time,
        event_source_url,
        custom_data,
        user_agent,
      } = body;

      // Hash user data for matching (IP + UA = basic matching)
      const clientIP =
        request.headers.get('CF-Connecting-IP') ||
        request.headers.get('X-Forwarded-For') ||
        '';
      const ua = user_agent || request.headers.get('User-Agent') || '';
      const fbp = extractCookie(request, '_fbp');
      const fbc = extractCookie(request, '_fbc');

      const hashedIP = await sha256(clientIP);
      const event = {
        event_name,
        event_time: event_time || Math.floor(Date.now() / 1000),
        event_id,
        event_source_url:
          event_source_url || 'https://nottingville.space',
        action_source: 'website',
        user_data: {
          client_ip_address: clientIP,
          client_user_agent: ua,
          ...(fbp && { fbp }),
          ...(fbc && { fbc }),
        },
        ...(custom_data && { custom_data }),
      };

      const metaURL = `https://graph.facebook.com/${API_VERSION}/${PIXEL_ID}/events`;
      const metaRes = await fetch(metaURL, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          data: [event],
          access_token: env.META_ACCESS_TOKEN,
        }),
      });

      const metaBody = await metaRes.json();

      return new Response(JSON.stringify({ ok: true, meta: metaBody }), {
        status: 200,
        headers: {
          'Content-Type': 'application/json',
          ...corsHeaders('https://nottingville.space'),
        },
      });
    } catch (err) {
      return new Response(
        JSON.stringify({ ok: false, error: err.message }),
        {
          status: 500,
          headers: {
            'Content-Type': 'application/json',
            ...corsHeaders('https://nottingville.space'),
          },
        }
      );
    }
  },
};

function corsHeaders(origin) {
  return {
    'Access-Control-Allow-Origin': origin,
    'Access-Control-Allow-Methods': 'POST, OPTIONS',
    'Access-Control-Allow-Headers': 'Content-Type',
  };
}

function extractCookie(request, name) {
  const cookieHeader = request.headers.get('Cookie') || '';
  const match = cookieHeader.match(new RegExp(`${name}=([^;]+)`));
  return match ? match[1] : null;
}

async function sha256(str) {
  const buf = await crypto.subtle.digest(
    'SHA-256',
    new TextEncoder().encode(str)
  );
  return Array.from(new Uint8Array(buf))
    .map((b) => b.toString(16).padStart(2, '0'))
    .join('');
}
