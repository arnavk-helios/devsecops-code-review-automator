import { NextResponse } from 'next/server';
import sqlite3 from 'sqlite3';
import { open } from 'sqlite';
import path from 'path';
import fs from 'fs';

export async function GET() {
  try {
    const dbPath = path.resolve(process.cwd(), '../audit_logs.db');

    // Verify if database file exists
    if (!fs.existsSync(dbPath)) {
      return NextResponse.json({ error: `Database not found at ${dbPath}` }, { status: 404 });
    }

    const db = await open({
      filename: dbPath,
      driver: sqlite3.Database
    });

    // Create table if it does not exist yet to avoid query errors
    await db.exec(`
      CREATE TABLE IF NOT EXISTS scans (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        pr_number INTEGER,
        agent_decisions TEXT,
        security_flags TEXT
      )
    `);

    const logs = await db.all('SELECT * FROM scans ORDER BY id DESC LIMIT 50');
    await db.close();

    return NextResponse.json(logs);
  } catch (error: any) {
    console.error("API Route Error:", error);
    return NextResponse.json({ error: error.message || 'Database query failed' }, { status: 500 });
  }
}