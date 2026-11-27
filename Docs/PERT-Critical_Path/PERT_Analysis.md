## PERT Analysis and Critical Path

As part of our course C07095  Real Estate  Data Analysis  Tool Project we have prepared PERT analysis 
to  Plan the activities involved in completing the project

Our project includes different areas such as data collection, data processing, property management, analytics, system 
integration and testing. These activities need to be organized because some tasks depend on others, while some 
can be  completed at same time. 

we use PERT to understand these dependencies and estimates how long the project activities 
may take.

## Project Schedule 
The project is organized into three sprints , with each sprint  planned for two weeks.
Project start date : 23rd Nov 2026
Final Submission Date: $th January 2027
Total Sprints: 3 
Duration of Each Sprint : 2 Weeks
Time Estimation
For the PERT analysis, we use three estimates for each activity.


For each activity, we use three different time estimates.

- *Optimistic (O):* The time needed if everything goes as planned.
- *Most Likely (M):* The time we normally expect the activity to take.
- *Pessimistic (P):* The time needed if problems or delays occur.

The expected time is calculated using the following PERT formula:

TE = (O + 4M + P) / 6

This calculation gives us an expected duration for each activity.

## Project Activities and Dependencies

We divided the project work into individual activities and assigned an ID to each activity, from A to BB.

The activities cover the main development and documentation work. We also included predecessor information to show which tasks depend on earlier activities.

This helps us understand the order of the work and identify tasks that can be completed in parallel.

The full activity list and time estimates are recorded in PERT_Activities.csv.

## PERT Diagram

The PERT diagram gives us a visual overview of the project activities and their connections. It helps us follow the planned order of work and understand how one activity can affect another.

The diagram is included in this folder as PERT_Diagram.png.

Critical Path Analysis

The critical path is the longest sequence of dependent activities in the project network. It helps us identify the activities that directly affect the overall project completion time.

Activities on the critical path have zero total slack. This means that delaying one of these activities may also delay the project.

The final critical path, project duration and slack values will be recorded after checking the activity dependencies and completing the calculations.

## Assumptions

The following points were considered when preparing the PERT plan:

- Activity durations are estimated in working days.
- The estimates are planning values and may need adjustments as the project progresses.
- Activities are arranged according to their dependencies.
- Some tasks may be completed at the same time.
- The project schedule needs to account for weekends and university holidays.

## Conclusion

Preparing the PERT analysis gives us a clearer understanding of the different activities involved in our project. It helps us organise the work, identify dependencies and understand which tasks need more attention.

We can use the PERT diagram and critical path calculations to monitor the planned schedule and work towards completing the project before the submission deadline.