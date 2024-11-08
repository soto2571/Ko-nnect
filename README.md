# ko-nnect

`ko-nnect` is a web application designed to streamline employee shift and schedule management. With an intuitive interface and advanced features, it enables both employees and administrators to manage and view schedules effectively.

## Table of Contents

- [ko-nnect](#ko-nnect)
  - [Table of Contents](#table-of-contents)
  - [Installation](#installation)
  - [Usage](#usage)
  - [Features](#features)
  - [Contributing](#contributing)
  - [License](#license)
  - [Contact](#contact)
    - [TEAM](#team)
  - [History and Acknowledgments](#history-and-acknowledgments)

## Installation

Follow these steps to set up the development environment for ko-nnect:

1. Clone the repository:

   ```bash
   git clone https://github.com/tu-usuario/ko-nnect.git
   cd ko-nnect
   ```

2. Create and activate a virtual environment:

   ```bash
   python3 -m venv venv
   source venv/bin/activate
   ```

3. Install the dependencies:

   ```bash
   pip install -r requirements.txt
   ```

4. Configure environment variables: Create a `.env` file in the project’s root directory and add the required variables.

5. Perform database migrations:

   ```bash
   flask db upgrade
   ```

6. Start the application:
   ```bash
   flask run
   ```

## Usage

To start the application, ensure the virtual environment is active and run:

```bash
flask run
```

## Features

- **Employee Login:** Employees can log in from their devices to instantly view their schedules.
- **Shift and Holiday Calendar:** View a shift calendar up to three weeks in advance, including public holidays in Puerto Rico.
- **Personalized Employee Access:** Administrators create unique credentials for each employee, enabling secure access to their schedules.
- **Two-Week Schedule View:** Employees can view a list of their current and upcoming shifts for the next 14 days.
- **Admin Dashboard:** A centralized panel for administrators to manage employee accounts and schedules.

## Contributing

If you’d like to contribute to `ko-nnect`, follow these steps:

1.  Fork the repository
2.  Create a new branch:

        git checkout -b feature/new-feature

3.  Make your changes and commit them:

        git commit -am 'Add new feature'

4.  Push your changes:

        git push origin feature/new-feature

5.  Open a Pull Request.

## License

This project is licensed under the MIT License. See the LICENSE file for more details.

## Contact

For more information, feel free to reach out to the team.

### TEAM

- [Sebastian Soto](https://github.com/soto2571)
- [Jose Mendez](https://github.com/jjmendezrodriguez)
- [Abdiel Rodriguez](https://github.com/Abdieljrg)

## History and Acknowledgments

Working on ko-nnect has been an incredibly rewarding experience for the entire team. From the beginning of the project, we have learned and grown both professionally and personally. Through collaboration and teamwork, we have overcome challenges and achieved our goals.

We would like to extend our heartfelt thanks to Holberton for providing the education and tools necessary to complete this project. Their support and guidance have been instrumental in our development as software developers.

**_Thank you, Holberton!_**

**_¡Gracias, Holberton!_**
