import jwt from 'jsonwebtoken';

import { config } from "dotenv";
config()

function generateAccessToken(user_id) {
    return jwt.sign(
      { id: user_id},
      process.env.KEY,
      { expiresIn: process.env.KEY_EXPIRE_DATE, algorithm: 'HS256' }
    );
}

function generateRefreshToken(user_id) {
    return jwt.sign(
        { id: user_id },
        process.env.REFRESH_KEY,
        { expiresIn: process.env.REFRESH_KEY_EXPIRE_DATE, algorithm: 'HS256' }
    );
}

export { generateAccessToken, generateRefreshToken };
