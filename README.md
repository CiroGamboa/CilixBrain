# CilixBrain
CilixBrain is a robotic system capable of capturing data through a camera and communicate via WiFi.

This program finds the route for a robot to follow so in this way it can optimize its sources.

To find the way:
1. The video is analized to identify the objects the robot has seen.
2. For each identified object the distance towards the robot and the angle is calculated.
3. With the list of elements, the graph is represented as a complete graph.
4. The Christofides algorithm that determines the route is executed.
5. It is created for use in mobile manipulative robots that execute the task of collecting objects.

Inspired by space exploration robots.

- Alix Angarita y Ciro Gamboa


UPB - Faculty of system and computing engineering
