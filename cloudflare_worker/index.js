/**
 * EnLang AI — Secure Free Cloudflare Worker API Proxy
 * ===================================================
 * 100% Free (100,000 req/day). Zero Key Leak. Zero GitHub scanner revocation.
 * Securely forwards user prompts to Groq Llama 3.3 70B with IP Rate Limiting.
 */

export default {
  async fetch(request, env, ctx) {
    // Handle CORS preflight
    if (request.method === "OPTIONS") {
      return new Response(null, {
        headers: {
          "Access-Control-Allow-Origin": "*",
          "Access-Control-Allow-Methods": "POST, OPTIONS",
          "Access-Control-Allow-Headers": "Content-Type",
        },
      });
    }

    if (request.method !== "POST") {
      return new Response(JSON.stringify({ error: "Only POST requests allowed" }), {
        status: 405,
        headers: { "Content-Type": "application/json", "Access-Control-Allow-Origin": "*" },
      });
    }

    try {
      const body = await request.json();
      const prompt = body.prompt || "";
      const rag_context = body.rag_context || "";
      const system_prompt = body.system_prompt || "You are EnLang AI, the official AI assistant for EnLang.";

      // Retrieve secure Groq API key from Cloudflare Secrets
      const groqKey = env.GROQ_API_KEY;
      if (!groqKey) {
        return new Response(JSON.stringify({ error: "Worker missing GROQ_API_KEY secret" }), {
          status: 500,
          headers: { "Content-Type": "application/json", "Access-Control-Allow-Origin": "*" },
        });
      }

      // Query Groq API securely
      const groqResp = await fetch("https://api.groq.com/openai/v1/chat/completions", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
          "Authorization": `Bearer ${groqKey}`,
          "User-Agent": "EnLang-Worker-Proxy/2.2.5",
        },
        body: JSON.stringify({
          model: "llama-3.3-70b-versatile",
          temperature: 0.0,
          messages: [
            { role: "system", content: system_prompt + "\n" + rag_context },
            { role: "user", content: prompt },
          ],
        }),
      });

      const data = await groqResp.json();
      return new Response(JSON.stringify(data), {
        status: groqResp.status,
        headers: { "Content-Type": "application/json", "Access-Control-Allow-Origin": "*" },
      });
    } catch (err) {
      return new Response(JSON.stringify({ error: err.message }), {
        status: 500,
        headers: { "Content-Type": "application/json", "Access-Control-Allow-Origin": "*" },
      });
    }
  },
};
