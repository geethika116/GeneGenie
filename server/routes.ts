import type { Express, Request, Response } from "express";
import { createServer, type Server } from "http";
import { storage } from "./storage";
import { createProxyMiddleware } from "http-proxy-middleware";

export async function registerRoutes(app: Express): Promise<Server> {
  // Proxy all non-API requests to Streamlit running on port 8501
  // This makes the Streamlit app the default page
  const streamlitPort = process.env.STREAMLIT_PORT || "8501";
  const streamlitProxy = createProxyMiddleware({
    target: `http://localhost:${streamlitPort}`,
    changeOrigin: true,
    ws: true, // Enable WebSocket proxying for Streamlit's live updates
    on: {
      error: (err, req, res) => {
        console.error("Streamlit proxy error:", err.message);
        if (res && typeof (res as any).writeHead === 'function') {
          (res as any).writeHead(503, { 'Content-Type': 'text/html' });
          (res as any).end(`
            <html>
              <head><title>Streamlit Not Running</title></head>
              <body style="font-family: system-ui; padding: 2rem; max-width: 600px; margin: 0 auto;">
                <h1>🧬 Gene Genie</h1>
                <p>The Streamlit application is not running.</p>
                <p>Please start it with: <code>streamlit run main.py --server.port ${streamlitPort}</code></p>
              </body>
            </html>
          `);
        }
      },
    },
  });

  // Proxy root and all Streamlit routes to the Streamlit app
  app.use("/", streamlitProxy);

  // Add your API routes here (they should be added BEFORE the proxy above)
  // Example:
  // app.get("/api/users", async (req, res) => {
  //   const users = await storage.getAllUsers();
  //   res.json(users);
  // });

  const httpServer = createServer(app);
  return httpServer;
}
