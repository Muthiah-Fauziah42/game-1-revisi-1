// Accept standard preview hosts as well as Next.js CLI flags.
import { spawn } from "node:child_process";
const input = process.argv.slice(2);
const args = ["dev", "--webpack", "--hostname", "0.0.0.0"];
for (let i = 0; i < input.length; i++) {
  if (input[i] === "--host") {
    i++;
    continue;
  }
  if (input[i] === "--strictPort") continue;
  args.push(input[i]);
}
const child = spawn(
  process.execPath,
  ["node_modules/next/dist/bin/next", ...args],
  { stdio: "inherit" },
);
for (const signal of ["SIGINT", "SIGTERM"])
  process.on(signal, () => child.kill(signal));
child.on("exit", (code) => process.exit(code ?? 0));
