<!doctype html>
<html lang="en">
<head>
  <meta charset="utf-8" />
  <meta name="viewport" content="width=device-width,initial-scale=1" />
  <title>Mini-Projects • Repository</title>

  <!-- Optional Google font -->
  <link href="https://fonts.googleapis.com/css2?family=Inter:wght@300;400;600;700&display=swap" rel="stylesheet">

  <style>
    :root{
      --bg:#0b0f14;
      --card:#0f161b;
      --muted:#93a3b2;
      --accent:#60a5fa;
      --glass:rgba(255,255,255,0.03);
      --border: rgba(255,255,255,0.04);
    }
    *{box-sizing:border-box}
    body{
      margin:0;
      font-family: "Inter", system-ui, -apple-system, "Segoe UI", Roboto, "Helvetica Neue", Arial;
      background: linear-gradient(180deg,#07101a 0%, #07121a 100%);
      color:#e6eef6;
      -webkit-font-smoothing:antialiased;
      -moz-osx-font-smoothing:grayscale;
      line-height:1.5;
      padding:28px;
    }

    .container{
      max-width:1000px;
      margin:0 auto;
    }

    header{
      display:flex;
      align-items:center;
      gap:18px;
      margin-bottom:22px;
    }
    .logo{
      width:68px;
      height:68px;
      display:grid;
      place-items:center;
      border-radius:12px;
      background:linear-gradient(135deg,#1e293b,#0ea5a9);
      box-shadow:0 6px 20px rgba(2,6,23,0.6), inset 0 -6px 20px rgba(255,255,255,0.03);
      font-weight:700;
      color:white;
      font-size:22px;
    }
    h1{margin:0;font-size:20px}
    p.lead{margin:6px 0 0;color:var(--muted)}

    .grid{
      display:grid;
      grid-template-columns: 1fr 320px;
      gap:20px;
      margin-top:18px;
    }

    /* main card */
    .card{
      background:var(--card);
      border:1px solid var(--border);
      border-radius:12px;
      padding:18px;
      box-shadow: 0 6px 18px rgba(2,6,23,0.45);
    }

    h2{margin:0 0 8px 0;font-size:16px}
    .muted{color:var(--muted);font-size:13px;margin-bottom:10px}

    .section{
      margin-bottom:16px;
    }

    /* file list */
    .file-list{
      display:grid;
      gap:8px;
      margin-top:8px;
    }
    .file{
      display:flex;
      align-items:center;
      justify-content:space-between;
      padding:10px 12px;
      background:var(--glass);
      border-radius:8px;
      border:1px solid rgba(255,255,255,0.02);
      font-size:14px;
    }
    .file .name{display:flex;gap:10px;align-items:center}
    .chip{
      font-size:12px;
      padding:6px 8px;
      border-radius:999px;
      background: rgba(255,255,255,0.03);
      color:var(--muted);
    }

    /* project cards list */
    .projects{
      display:grid;
      gap:10px;
      margin-top:10px;
    }
    .proj{
      padding:12px;
      border-radius:10px;
      background: linear-gradient(180deg, rgba(255,255,255,0.015), transparent);
      border:1px solid rgba(255,255,255,0.02);
    }
    .proj h3{margin:0;font-size:14px}
    .proj p{margin:6px 0 0 0;color:var(--muted);font-size:13px}

    /* right column */
    aside .card{position:sticky;top:28px}
    .badge{
      display:inline-block;
      padding:6px 10px;
      font-size:13px;
      border-radius:999px;
      background:rgba(96,165,250,0.12);
      color:var(--accent);
      margin-right:8px;
    }

    .features li{margin-bottom:8px;color:var(--muted)}

    footer{
      margin-top:18px;color:var(--muted);
      font-size:13px;text-align:center;
    }

    /* Responsive */
    @media (max-width:980px){
      .grid{grid-template-columns:1fr; padding-bottom:30px}
      aside .card{position:static}
    }
  </style>
</head>
<body>
  <div class="container">
    <header>
      <div class="logo">MP</div>
      <div>
        <h1>Mini-Projects <span style="font-size:16px;opacity:0.9">🚀</span></h1>
        <p class="lead">A collection of small but powerful projects implemented in <strong>Python</strong>, <strong>C</strong>, and <strong>C++</strong>.
        Covering Cybersecurity, Utilities, Games, and Data Processing — great for demos and learning.</p>
      </div>
    </header>

    <div class="grid">
      <!-- main column -->
      <main>
        <div class="card">
          <div class="section">
            <h2>📂 Repository Structure</h2>
            <p class="muted">Top-level organization and quick file list.</p>

            <div style="display:flex;gap:18px;flex-wrap:wrap;margin-top:10px">
              <div style="min-width:260px">
                <strong>Cyber-security Projects</strong>
                <div class="file-list" style="margin-top:8px">
                  <div class="file"><div class="name">GUI-Password-Checker.py</div><div class="chip">GUI</div></div>
                  <div class="file"><div class="name">Password-Checker.py</div><div class="chip">Security</div></div>
                  <div class="file"><div class="name">Port-Scanner.py</div><div class="chip">Network</div></div>
                  <div class="file"><div class="name">keylogger.py</div><div class="chip">Research</div></div>
                  <div class="file"><div class="name">user_authentication_hashlib_mysql.py</div><div class="chip">DB</div></div>
                  <div class="file"><div class="name">web_scrape.py</div><div class="chip">Scraping</div></div>
                </div>
              </div>

              <div style="min-width:260px">
                <strong>Other Projects</strong>
                <div class="file-list" style="margin-top:8px">
                  <div class="file"><div class="name">calculator.cpp</div><div class="chip">C++</div></div>
                  <div class="file"><div class="name">career_recommendation.py</div><div class="chip">ML-ish</div></div>
                  <div class="file"><div class="name">expenses-tracker.py</div><div class="chip">Utility</div></div>
                  <div class="file"><div class="name">medico_initial_screening.c</div><div class="chip">C</div></div>
                  <div class="file"><div class="name">merge_multiple_array.cpp</div><div class="chip">C++</div></div>
                  <div class="file"><div class="name">tic-tac-toe.c</div><div class="chip">Game</div></div>
                  <div class="file"><div class="name">to-do_list.py</div><div class="chip">CLI</div></div>
                </div>
              </div>
            </div>
          </div>

          <div class="section">
            <h2>🛡️ Cyber Security Projects</h2>
            <p class="muted">Short descriptions — use these in your README to quickly explain each script.</p>

            <div class="projects">
              <div class="proj">
                <h3>GUI-Password-Checker.py</h3>
                <p>A graphical tool to check password strength using complexity rules and visual feedback.</p>
              </div>

              <div class="proj">
                <h3>Password-Checker.py</h3>
                <p>Checks whether a password has been compromised (e.g., via HaveIBeenPwned-style checks).</p>
              </div>

              <div class="proj">
                <h3>Port-Scanner.py</h3>
                <p>Scans target IP/host ports using sockets to find open services (basic network scanning).</p>
              </div>

              <div class="proj">
                <h3>keylogger.py</h3>
                <p>Monitors keystrokes for educational demonstration and logging (use ethically & legally).</p>
              </div>

              <div class="proj">
                <h3>user_authentication_hashlib_mysql.py</h3>
                <p>User authentication with securely hashed passwords stored in a MySQL database.</p>
              </div>

              <div class="proj">
                <h3>web_scrape.py</h3>
                <p>Simple scraping utility using BeautifulSoup to collect and process web data.</p>
              </div>
            </div>
          </div>

          <div class="section">
            <h2>🛠️ Utility & Other Projects</h2>
            <div class="projects">
              <div class="proj">
                <h3>calculator.cpp</h3>
                <p>Basic arithmetic calculator implemented in C++ (console-based).</p>
              </div>

              <div class="proj">
                <h3>career_recommendation.py</h3>
                <p>Suggests career options based on user inputs about interests and skills.</p>
              </div>

              <div class="proj">
                <h3>expenses-tracker.py</h3>
                <p>Track daily expenses and generate a simple summary report for budgeting.</p>
              </div>

              <div class="proj">
                <h3>medico_initial_screening.c</h3>
                <p>Basic medical screening helper that collects inputs and outputs recommended actions.</p>
              </div>

              <div class="proj">
                <h3>merge_multiple_array.cpp</h3>
                <p>Merges multiple arrays into a single sorted array efficiently.</p>
              </div>

              <div class="proj">
                <h3>tic-tac-toe.c</h3>
                <p>Classic Tic-Tac-Toe two-player game implemented in C (terminal).</p>
              </div>

              <div class="proj">
                <h3>to-do_list.py</h3>
                <p>Command-line to-do list manager to add, remove, and list daily tasks.</p>
              </div>
            </div>
          </div>

          <div class="section">
            <h2>✅ Features</h2>
            <ul class="features" style="padding-left:18px;margin-top:8px">
              <li>Covers multiple languages: <strong>Python</strong>, <strong>C</strong>, and <strong>C++</strong>.</li>
              <li>Focus areas include Cybersecurity, Automation, Utilities, and small Games.</li>
              <li>Designed to be beginner-friendly with clear, well-commented examples.</li>
            </ul>
          </div>

          <div class="section">
            <h2>📌 How to run</h2>
            <p class="muted">Clone repository, then run Python scripts or compile C/C++ files as usual.</p>

            <pre style="background:rgba(0,0,0,0.25);padding:12px;border-radius:8px;font-size:13px;color:#dbeafe;overflow:auto">
git clone https://github.com/your-username/Mini-Projects-.git
# Python
python3 script_name.py

# C / C++
gcc file.c -o out && ./out
g++ file.cpp -o out && ./out
            </pre>
          </div>

          <div class="section">
            <h2>📜 License</h2>
            <p class="muted">This repository is for educational purposes only. Use responsibly and ethically.
            For anything involving monitoring, scanning or security tools—obtain consent and follow laws.</p>
          </div>

        </div>
      </main>

      <!-- right column -->
      <aside>
        <div class="card">
          <div style="display:flex;align-items:center;justify-content:space-between">
            <div>
              <span class="badge">Python</span>
              <span class="badge">C</span>
              <span class="badge">C++</span>
            </div>
            <div style="text-align:right">
              <div style="font-weight:600">Mini-Projects</div>
              <div class="muted" style="font-size:12px">A curated learning collection</div>
            </div>
          </div>

          <hr style="border:none;border-top:1px solid rgba(255,255,255,0.03);margin:12px 0">

          <div style="display:flex;gap:8px;flex-wrap:wrap">
            <div style="flex:1 1 100%;"><strong>Quick tips</strong></div>
            <div style="flex:1 1 100%" class="muted">
              - Add README inside each project with usage & dependencies.<br>
              - Add license file and contribution guide if you want others to help.<br>
              - Consider adding screenshots or GIFs for GUI projects.
            </div>
          </div>

          <hr style="border:none;border-top:1px solid rgba(255,255,255,0.03);margin:12px 0">

          <div>
            <strong>Contact</strong>
            <p class="muted" style="margin:8px 0 0">Your Name — <a href="#" style="color:var(--accent);text-decoration:none">github.com/your-username</a></p>
          </div>
        </div>
      </aside>
    </div>

    <footer>
      Built with ❤ — feel free to copy this HTML into your repo as <strong>README.html</strong>.
    </footer>
  </div>
</body>
</html>
