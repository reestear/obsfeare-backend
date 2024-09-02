import bcrypt from "bcrypt";
import express from "express";
import jwt from "jsonwebtoken";
import { preRegister } from "../middlewares/auth_middleware.js";
import User from "../models/User.js";
import { generateAccessToken, generateRefreshToken } from "../utils/auth/index.js";

import { config } from "dotenv";
config()

const router = express.Router();

// Register route
router.post("/register", preRegister, async (req, res) => {
  // Registration logic
  const { username, email } = req.body.user;
  try {
    const user = await new User({
      username: username,
      email: email,
      password: req.hashedPassword,
    });
    await user.save();
    const userId = user._id;

    const actoken = generateAccessToken(userId);
    const refreshToken = generateRefreshToken(userId);

    res.cookie('refreshToken', refreshToken, {
      httpOnly: true,
      secure: true,
      sameSite: 'Strict',
      maxAge: 7 * 24 * 60 * 60 * 1000
    });

    res
      .status(201)
      .json({ actoken: actoken, message: "Successful Registration" });
  } catch (err) {
    res.sendStatus(500);
    console.log(err.message);
  }
});

// Login route
router.get("/login/:email/:password", async (req, res) => {

  try {
    const { email, password } = req.params;

    if (!(await User.findOne({ email: email })))
      return res.status(401).json({ message: "Account doesn't exist" });

    const user = await User.findOne({ email: email });
    const hashedPassword = user.password;

    if (await bcrypt.compare(password, hashedPassword)) {
      const actoken = generateAccessToken(user._id);
      const refreshToken = generateRefreshToken(user._id);

      res.cookie('refreshToken', refreshToken, {
        httpOnly: true,
        secure: true,
        sameSite: 'Strict',
        maxAge: 7 * 24 * 60 * 60 * 1000
      });

      res.status(200).json({ actoken: actoken, message: "Succesful LogIn" });
    } else return res.status(403).json({ message: "Incorrect Password" });
  } catch (err) {
    console.log(err.message);
    res.status(500).json({ message: "Something Went Wrong in the Server" });
  }
});

// Refresh token route
router.post("/refresh", async (req, res) => {
  const refreshToken = req.body.refreshToken;
  if (!refreshToken) return res.status(401).json({ message: "No refresh token" });

  jwt.verify(refreshToken, process.env.REFRESH_KEY, (err, user) => {
    if (err) return res.status(403).json({ message: "Invalid token" });

    const actoken = generateAccessToken(user.id);
    const refreshToken = generateRefreshToken(user.id);
    
    res.cookie('refreshToken', refreshToken, {
      httpOnly: true,
      secure: true,
      sameSite: 'Strict',
      maxAge: 7 * 24 * 60 * 60 * 1000
    });

    res.status(200).json({ actoken: actoken });
  });
})

export default router;
