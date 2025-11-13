"""Liatrio brand CSS styling for HTML output."""

LIATRIO_CSS = """        :root {
            /* Liatrio Brand Colors - Dark Theme */
            --bg-primary: #111111;
            --bg-secondary: #1e1e1e;
            --bg-tertiary: #3a3a3a;
            --text-primary: #ffffff;
            --text-secondary: #eeeeee;
            --text-muted: #9c9c9c;
            --accent-primary: #24AE1D;
            --accent-secondary: #89DF00;
            --accent-lagoon: #00C1DB;
            --accent-deep-sea: #007DAA;
            --accent-hot-red: #FF5100;
            --accent-flame: #FFAA00;
            --border-color: #444444;
            --code-bg: #1e1e1e;
            --code-border: #3a3a3a;
        }

        * {
            box-sizing: border-box;
        }

        body {
            font-family: 'DM Sans', -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
            background-color: var(--bg-primary);
            color: var(--text-primary);
            line-height: 1.6;
            margin: 0;
            padding: 0;
            font-size: 16px;
        }

        .container {
            max-width: 1200px;
            margin: 0 auto;
            padding: 2rem;
        }

        /* Typography */
        h1,
        h2,
        h3,
        h4,
        h5,
        h6 {
            font-family: 'Clash Display', 'Anybody', 'DM Sans', sans-serif;
            font-weight: 700;
            color: var(--text-primary);
            margin-top: 2rem;
            margin-bottom: 1rem;
            line-height: 1.2;
        }

        h1 {
            font-size: 2.5rem;
            border-bottom: 3px solid var(--accent-primary);
            padding-bottom: 0.5rem;
        }

        h2 {
            font-size: 2rem;
            border-bottom: 2px solid var(--border-color);
            padding-bottom: 0.3rem;
        }

        h3 {
            font-size: 1.5rem;
            color: var(--accent-secondary);
        }

        h4 {
            font-size: 1.25rem;
            color: var(--accent-lagoon);
        }

        p {
            margin-bottom: 1rem;
            color: var(--text-secondary);
        }

        /* Links */
        a {
            color: var(--accent-primary);
            text-decoration: none;
            transition: color 0.2s ease;
        }

        a:hover {
            color: var(--accent-secondary);
            text-decoration: underline;
        }

        /* Lists */
        ul,
        ol {
            margin-bottom: 1rem;
            padding-left: 2rem;
        }

        li {
            margin-bottom: 0.5rem;
            color: var(--text-secondary);
        }

        /* Code */
        code {
            background-color: var(--code-bg);
            color: var(--accent-secondary);
            padding: 0.2rem 0.4rem;
            border-radius: 4px;
            font-family: 'Monaco', 'Menlo', 'Ubuntu Mono', monospace;
            font-size: 0.9em;
            border: 1px solid var(--code-border);
            white-space: pre-wrap;
            word-wrap: break-word;
            overflow-wrap: break-word;
            word-break: break-all;
            max-width: 100%;
        }

        pre {
            background-color: var(--code-bg);
            border: 1px solid var(--code-border);
            border-radius: 8px;
            padding: 1rem;
            overflow-x: auto;
            overflow-wrap: break-word;
            word-wrap: break-word;
            white-space: pre-wrap;
            word-break: break-all;
            margin-bottom: 1rem;
            max-width: 100%;
        }

        pre code {
            background: none;
            border: none;
            padding: 0;
            color: var(--text-primary);
            white-space: pre-wrap;
            word-wrap: break-word;
            overflow-wrap: break-word;
            word-break: break-all;
            max-width: 100%;
        }

        /* Blockquotes */
        blockquote {
            border-left: 4px solid var(--accent-primary);
            margin: 1rem 0;
            padding: 0.5rem 1rem;
            background-color: var(--bg-secondary);
            color: var(--text-muted);
        }

        /* Tables */
        table {
            width: 100%;
            border-collapse: collapse;
            margin-bottom: 1rem;
            background-color: var(--bg-secondary);
        }

        th,
        td {
            padding: 0.75rem;
            text-align: left;
            border-bottom: 1px solid var(--border-color);
        }

        th {
            background-color: var(--bg-tertiary);
            color: var(--text-primary);
            font-weight: 600;
        }

        td {
            color: var(--text-secondary);
        }

        tr:hover {
            background-color: var(--bg-tertiary);
        }

        /* Horizontal Rule */
        hr {
            border: none;
            height: 2px;
            background: linear-gradient(to right, var(--accent-primary), var(--accent-lagoon));
            margin: 2rem 0;
        }

        /* Status Indicators */
        .status-pass {
            color: var(--accent-primary);
            font-weight: 600;
        }

        .status-fail {
            color: var(--accent-hot-red);
            font-weight: 600;
        }

        .status-warning {
            color: var(--accent-flame);
            font-weight: 600;
        }

        /* Proof artifacts and code references */
        .code-ref {
            background-color: var(--bg-tertiary);
            padding: 0.1rem 0.3rem;
            border-radius: 3px;
            font-family: monospace;
            font-size: 0.85em;
        }

        /* Section styling */
        .executive-summary {
            background: linear-gradient(135deg, var(--bg-secondary) 0%, var(--bg-tertiary) 100%);
            padding: 1.5rem;
            border-radius: 8px;
            margin-bottom: 2rem;
            border-left: 5px solid var(--accent-primary);
        }

        /* Metrics styling */
        .metrics {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
            gap: 1rem;
            margin: 1rem 0;
        }

        .metric-card {
            background-color: var(--bg-secondary);
            padding: 1rem;
            border-radius: 6px;
            border: 1px solid var(--border-color);
        }

        /* Strong text styling */
        strong {
            color: var(--accent-primary);
            font-weight: 600;
        }

        /* Table of Contents */
        .table-of-contents {
            background-color: var(--bg-secondary);
            border: 1px solid var(--border-color);
            border-radius: 8px;
            padding: 1.5rem;
            margin: 2rem 0;
        }

        .table-of-contents h2 {
            margin-top: 0;
            color: var(--accent-primary);
            border-bottom: 1px solid var(--border-color);
            padding-bottom: 0.5rem;
        }

        .toc-list {
            list-style: none;
            padding-left: 0;
            margin: 0;
        }

        .toc-list ul {
            list-style: none;
            padding-left: 0;
            margin: 0.25rem 0 0.25rem 1.5rem;
            border-left: 2px solid var(--border-color);
            position: relative;
        }

        .toc-list ul::before {
            content: '';
            position: absolute;
            left: -2px;
            top: 0;
            bottom: 0;
            width: 2px;
            background-color: var(--bg-secondary);
        }

        .toc-list li {
            margin-bottom: 0.25rem;
            padding: 0;
            position: relative;
            line-height: 1.6;
        }

        .toc-list li::before {
            content: '├─';
            position: absolute;
            left: -1.5rem;
            color: var(--accent-lagoon);
            font-weight: normal;
        }

        .toc-list > li::before {
            display: none;
        }

        .toc-list ul > li:last-child::before {
            content: '└─';
        }

        .toc-list a {
            color: var(--text-secondary);
            text-decoration: none;
            transition: all 0.2s ease;
            display: inline-block;
            padding: 0.25rem 0.5rem;
            border-radius: 4px;
            margin-left: 0;
        }

        .toc-list a:hover {
            color: var(--accent-primary);
            background-color: var(--bg-tertiary);
            text-decoration: none;
        }

        /* User/Cursor ToC entries */
        .toc-legend {
            margin: 1rem 0;
            font-size: 0.9rem;
            text-align: center;
        }

        .legend-user {
            color: var(--accent-lagoon);
            font-weight: 600;
            margin-right: 1rem;
        }

        .legend-cursor {
            color: var(--accent-secondary);
            font-weight: 600;
        }

        .user-entry {
            border-radius: 8px;
            transition: all 0.2s ease;
        }

        .user-entry .toc-link {
            border-radius: 8px;
        }

        .user-entry .toc-link:hover {
            background-color: rgba(0, 193, 219, 0.1);
            transform: translateX(4px);
        }

        .cursor-entry {
            margin-bottom: 0.75rem;
            border-radius: 8px;
            transition: all 0.2s ease;
        }

        .cursor-entry .toc-link {
            border-radius: 8px;
        }

        .cursor-entry .toc-link:hover {
            background-color: rgba(137, 223, 0, 0.1);
            transform: translateX(4px);
        }

        .toc-link {
            text-decoration: none;
            font-weight: 600;
            display: block;
            padding: 0.75rem;
            transition: color 0.2s ease, background-color 0.2s ease, transform 0.2s ease;
        }

        .toc-user {
            color: var(--text-secondary);
        }

        .toc-user:hover {
            color: var(--accent-lagoon);
            text-decoration: underline;
        }

        .toc-cursor {
            color: var(--text-secondary);
        }

        .toc-cursor:hover {
            color: var(--accent-secondary);
            text-decoration: underline;
        }

        .speaker-label {
            font-weight: 700;
            display: inline-block;
            min-width: 80px;
            padding: 0.2rem 0.6rem;
            border-radius: 4px;
            margin-right: 0.5rem;
            font-size: 0.85em;
        }

        .toc-user .speaker-label {
            background-color: rgba(0, 193, 219, 0.2);
            color: var(--accent-lagoon);
            border: 1px solid var(--accent-lagoon);
        }

        .toc-cursor .speaker-label {
            background-color: rgba(137, 223, 0, 0.2);
            color: var(--accent-secondary);
            border: 1px solid var(--accent-secondary);
        }

        .toc-divider {
            color: var(--accent-lagoon);
            margin: 0 0.4rem;
            font-weight: 600;
            font-size: 1.1em;
            display: inline-block;
            text-decoration: none !important;
        }

        .cursor-entry .toc-divider {
            color: var(--accent-secondary);
        }

        .toc-link:hover .toc-divider {
            text-decoration: none !important;
        }

        .preview-text {
            font-weight: normal;
            font-style: italic;
            color: var(--text-muted);
            background-color: rgba(0, 193, 219, 0.1);
            padding: 0.2rem 0.5rem;
            border-radius: 4px;
            display: inline-block;
        }

        .cursor-entry .preview-text {
            background-color: rgba(137, 223, 0, 0.1);
        }

        .back-to-top {
            text-align: right;
            margin: -0.5rem 0 1rem 0;
            font-size: 0.85rem;
        }

        .back-to-top a {
            color: var(--text-muted);
            text-decoration: none;
            padding: 0.25rem 0.5rem;
            border-radius: 4px;
            background-color: var(--bg-tertiary);
            border: 1px solid var(--border-color);
            transition: all 0.2s ease;
        }

        .back-to-top a:hover {
            color: var(--accent-primary);
            background-color: var(--border-color);
            text-decoration: none;
        }

        /* Responsive design */
        @media (max-width: 768px) {
            .container {
                padding: 1rem;
            }

            h1 {
                font-size: 2rem;
            }

            h2 {
                font-size: 1.5rem;
            }
        }"""
