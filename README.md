README file for the SOEN341 group project - Team Omega

**In this file, you will see the following:**

1) Description of the Project 
2) Team Members and Roles 
3) Project Approach and Technology


**Description of the project**

In this project, we are tasked with creating a car rental application that will facilitate the process of renting vehicles for short periods, ranging from a few hours to a few weeks. Through this project, our team members will get to experience firsthand how a software project is managed using Github.

**Team Members and Roles**

Software Engineering Undergraduate(s):

_Daniel Cicciarelli,_
_Liam Halpin,_
_Maria Shanoudy-Farhood,_
_Matthew Kazemie_

As the name implies, software engineering focuses on the design of software applications and programs. These team members are the backbone of this project as they are most familiar with software applications and have had experience in both front end and back end development.

Computer Engineering Undergraduate(s):
_Maxime Pagé_

Computer engineering is a mix of software engineering and of hardware engineering. Although less experienced with software design, this team member is knowledgeable in many programming languages that will provide support to the other team members. 


**Project Approach and Technology**

1. Project Overview
 
 1.1 Project Objectives

  The goal of this project is to create a web application prototype or base for a car rental project. Users of this application can create accounts,
  browse vehicles, make reservations and modify/delete account or reservation specifics. This needs to be created using GitHub as a repository for our
  code and documentation.

 
 1.2 Scope

  This project will be a functioning web page. Users will be able to sign in or create a new account. With an account, users will to make a reservation. If 
  a user has an existing reservation, they will be able to view, modify and delete that reservation. If a user has an account, they will be able to view,
  modify and delete their account. They will be able to change passwords and change usernames (if the new username does not already exist).

  The website itself will consist of a home page with a list of available vehicles. Filters will be available to narrow down a users search. On the home
  page, there will be brief details on the cars. Selecting a car will bring the user to a new page with more details on the car, as well as the option to
  reserve the car. A database will store users, cars and reservations.

  System administators will be able to view, modify, and delete any existing user. They will be available to view, modify, and delete any existing
  reservation. They will also be available to view, modify and delete any existing car. System administrators will also be able to add new cars, new users
  and new reservations.

  Users will be able to review and rate the service, (ratings will also be stored in a database), and select a pickup location for certain cars.
 
 1.3 Target Audience
 
  We are looking to have two target audiences. Firstly, we are looking to target travellers to Montreal who are in need of a car to get around while they
  are here. Secondly, we are looking to target either travellers or locals who want to rent a luxury car for a shorter period of time. Of course, any 
  user must be 23 years old or older to rent a car.
 
 2. Project Approach
 
 2.1 Development Methodology
- Choose a development methodology (e.g., Agile, Waterfall) and
justify the selection based on project requirements.
 
 2.2 Project Timeline
 
 Refer to wiki for full details on project timeline.
 
 2.3 Collaboration and Communication

 Our team will be using Discord for the majority of our communication and using Github for the code and the seperation of tasks. We will also be meeting in person at least once per week. On Discord, calls and messages will be used.
 
 3. Technology Stack
 
 3.1 Backend Frameworks
 
 3.1.1 Spring Framework
 
 Spring is a java-based framework thats been around for over 20 years. The primary function of spring is to simplify the setup and configuration process,
 allowing users to focus more on the actual logic of the code rather than the syntax or setup process.

 Spring can potentially be a good option for us to use because of the community support. Despite Spring being around for a long time, its still one of the 
 most used frameworks out there. There are plenty of tutorials, guides, and videos online displaying Spring's features and how to use them. Spring seems to 
 be very easy to integrate to a project.
 
 Also, the fact that Spring is java-based is useful, as Java is a programming language that all of our team members are familiar with. Another useful 
 feature we can take advantage of with Spring is that it supports HTML, which will help us with the frontend work as well.

 Despite the support online, Spring is apparently difficult to learn and master. While we don't necessarily need to master Spring, if we're not able to
 take advantage of it's features, then it defeats the purpose of using it in the first place. Furthermore, it seems that it is very difficult to integrate
 databases with Spring, which is a major part of our project.

 To conclude Spring, its a viable option for us to use in our project. It's based in a language all of our group members are comfortable with, and can 
 support both fronted and backend. There is a huge community available for tutorials and questions, and it is very easy to integrate into a project. 
 Unfortunately, there are some downsides as well. Spring seems hard to learn, harder to master, and may cause issues for us when we try to integrate 
 databases to our project.
 
 3.1.2 Flask

Flask is a lightweight and versatile web development framework for     Python. It is simple and easy to use for beginners which makes it a good option to create prototypes for smaller web sites.

Flask is simple to use and flexible making it easy for beginners to use and create a website from it during their first-time    use. It is also a minimalistic web development frame when it comes to its web design. Flask comes with its own pros and cons that can change how you plan to create your website. A great thing about Flask is that it has a large and active community that and can help with any questions or difficulties that you may encounter while using Flask. There are a lot of tutorials on how to use flask on YouTube as well as websites to teach the different functions that are offered by flask. Flask can also be integrated with Python which is our backend language of choice. This can give us access to python libraries and framework. These libraries and frameworks give us access to some features that can simplify our workload for the creation of our website such as database management.
maintenance.

Flask's has more of a minimalist design while also containing beginner-friendly API which make it easy to learn and use for  beginners and first-time users. In Flask, you can access libraries of different back-end languages such as python which offers a lot more options for website design, management, and creation. Flask also has a small codebase compared to other frameworks which makes it more dependable than others and great for creating web site prototypes quickly as well as for making quick overhauls.

Flask's takes a more minimalistic approach to web development, which means that it lacks some features that other web development frames might have. Furthermore, compared to a more fully featured frameworks that uses Python like Django, Flask requires more manual setup such as having to connecte to python libraries for tasks such as database management and user authentication.
  - Use Cases
 
 3.1.3 Framework C
- Description: Brief overview of Framework C.
- Rationale:
  - Justification for choosing Framework C.
  - Consider factors such as community support, learning
curve, and extensibility.
- Qualitative Assessment:
  - Strengths
  - Weaknesses
  - Use Cases
 
 3.2 Frontend Frameworks
 
 3.2.1 Framework X
- Description: Brief overview of Framework X.
- Rationale:
  - Justification for choosing Framework X.
  - Consider factors such as user interface
capabilities, responsiveness, and cross-browser compatibility.
- Qualitative Assessment:
  - Strengths
  - Weaknesses
  - Use Cases
 
 3.2.2 Framework React.js
 
React.js is a JavaScript library for building interactive UIs (User Interface), and it was initially developed at Facebook to fix code maintainability issues. It utilized what are called "components" to make applications. These components are pieces of the UI that are fully programmable and which range from a simple button to the entire page.

First and foremost, many applications that people use in their daily lives are developed with React: notably, we have Facebook, Instragram, Netflix, NY Times, Yahoo! and even Khan Academy.
Secondly, React.js is considered the best frontend framework by many articles online, as well as reviewers who said they are more likely to re-use React.js than any other frameworks.
The components aforementioned are easily reusabable and the integrated React hooks makes writing them easy.
It should also be mentioned that React.js has an incredibly large support community as it is used for the largest social media apps.
 
In other words, React.js comes with very practical tools, such as components and hooks. The large community support is a key part of considering a framework as any problem we encounter might have already been solved.
However, React.js has a steep learning curve and it could be difficult for those with little to no knowledge of javascript to learn how to use it.
In terms of use cases, React.js is a perfect match for a single-page web application (take Facebook for example).
 
 3.2.3 Framework Z
- Description: Brief overview of Framework Z.
- Rationale:
  - Justification for choosing Framework Z.
  - Consider factors such as ease of integration,
component libraries, and developer experience.
- Qualitative Assessment:
  - Strengths
  - Weaknesses
  - Use Cases
 
 4. Integration and Interoperability
 
 4.1 Backend-Frontend Integration
- Outline the strategy for integrating the chosen backend and
frontend technologies.
 
 4.2 Third-Party Services
 
 The only third-party service we will use is an online database service. Right now, the application we are considering is mySQL, which we will use to store
 usernames, passwords, users, cars, reservations and ratings.
 
 5. Security Considerations
 
- Provide an overview of security measures and considerations for
both the backend and frontend.
 
 6. Conclusion
 
- Summarize the chosen project approach and technology stack,
highlighting key reasons for the selections.
