# ADR 2: Add Web-Based Visualization Demo with Flask

## Status
Accepted

## Context
The Mars Rover kata implementation was originally CLI-based. To improve accessibility and provide a more engaging demonstration, the team decided to add a web-based visualization. This allows users to input rover commands and see the results visually in their browser.

## Decision
We introduced a Flask-based web application (`webdemo/`) that:
- Accepts Mars Rover input in the same format as the CLI
- Uses the existing Python logic to process rover commands
- Returns the final rover positions as JSON
- Provides a static HTML/JavaScript frontend to visualize the plateau and rover positions on a grid using Canvas

## Consequences
### Positive
- Users can interact with the Mars Rover kata visually, making the demo more engaging
- The web demo reuses core logic, ensuring consistency between CLI and web
- Easy to run locally or in cloud dev environments (e.g., Codespaces)
- Lays groundwork for future enhancements (e.g., step-by-step animation)

### Negative
- Adds a dependency on Flask and basic frontend code
- Slightly increases project complexity and maintenance
