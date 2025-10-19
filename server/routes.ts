import type { Express } from "express";
import { createServer, type Server } from "http";
import { storage } from "./storage";

export async function registerRoutes(app: Express): Promise<Server> {
  // Add your API routes here
  // Example:
  // app.get("/api/users", async (req, res) => {
  //   const users = await storage.getAllUsers();
  //   res.json(users);
  // });

  const httpServer = createServer(app);
  return httpServer;
}
