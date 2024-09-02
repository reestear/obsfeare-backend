import cookieParser from "cookie-parser";
import cors from "cors";
import express, { json } from "express";
import authRoutes from "./routes/auth_routes.js";

import { config } from "dotenv";
config()

const app = express();

app.use(json());
app.use(cors());
app.use(cookieParser());

app.get("/", (req, res) => {
  console.log("Auth service is running!");
  res.json({message: "Auth service is running!"});
});

// Mount routes
app.use("/auth", authRoutes);

export default app;
