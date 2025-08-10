# Static Site Generator

This is a custom-built static site generator (SSG) that converts Markdown files into a static website. It is designed to be simple, extensible, and easy to use.

## Features

*   **Markdown-based content:** Write your pages in simple Markdown.
*   **Customizable templates:** Easily customize the look and feel of your site.
*   **Development server:** A live-reloading development server for a smooth writing experience.
*   **Extensible:** The modular architecture allows for easy extension and customization.

## Getting Started

To get started with this SSG, you'll need to have Python and Node.js installed.

1.  **Clone the repository:**
    ```bash
    git clone <repository-url>
    cd <repository-name>
    ```

2.  **Install Python dependencies:**
    ```bash
    pip install -r requirements.txt
    ```

3.  **Install Node.js dependencies:**
    ```bash
    cd sandbox/.web
    npm install
    ```

4.  **Run the development server:**
    ```bash
    python -m src.cli develop
    ```

## Usage

### Creating Content

To create a new page, simply add a new Markdown file (`.md`) to the `sandbox/app/pages` directory. The directory structure of the `pages` directory will be reflected in the URL structure of the generated site.


## Project Structure

*   `src/`: The main source code of the SSG.
    *   `cli.py`: The command-line interface for the SSG.
    *   `parser.py`: The Markdown parser.
    *   `export/py`: Main export file that compiles eveything before serving it.
    *   `core/`: Core components like the navbar, sidebar, and templates.
    *   `states/`: Centralized state folder to add interactivty for injected components.

*   `sandbox/`: A sample project using the SSG.
    *   `app/`: The application logic for the sandbox project.
    *   `pages/`: The content for the sandbox site.


## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.
