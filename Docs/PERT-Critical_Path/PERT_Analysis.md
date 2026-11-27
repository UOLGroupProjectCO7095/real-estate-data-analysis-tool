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
Final Submission Date: 4th January 2027
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
Critical Path Analysis

The critical path was identified by calculating the earliest start, earliest finish, latest start and latest finish times for each activity.

The expected duration of each activity was calculated using the PERT formula:

TE = (O + 4M + P) / 6

The total slack was calculated by subtracting the earliest start time from the latest start time.

Activities with zero total slack are considered critical activities because any delay in these activities may affect the overall project completion time.

Calculated Project Duration: 81.33 working days.

Critical Activities:

A → B → C → D → F → (G, H, I) → M → N → P → Q → R → T → U → AF → AJ → AK → AL → AM → AN → AP → AQ → AR → AS → AT → AZ → BB
Activities G, H and I are performed in parallel. All three have zero slack and must be completed before activity M can start.
Critical Path Findings:
* Total number of activities: 54.
* Expected project duration: 81.33 working days.
* Critical activities have zero total slack.
* Non-critical activities have positive total slack.
* Activities G, H and I can run in parallel.
* Delays in critical activities may affect the overall project completion time.
The critical path helps the team identify activities that require close monitoring and attention during project development.

PERT Activity Time and Slack Calculations

This section presents the calculated PERT expected duration, earliest start (ES), earliest finish (EF), latest start (LS), latest finish (LF), and total slack for all 54 project activities.

The calculations are based on the original activity estimates and predecessor relationships recorded in PERT_Activities.csv.
| Activity | TE | ES | EF | LS | LF | Slack |
|---|---:|---:|---:|---:|---:|---:|
| A | 3.00 | 0.00 | 3.00 | 0.00 | 3.00 | 0.00 |
| B | 3.00 | 3.00 | 6.00 | 3.00 | 6.00 | 0.00 |
| C | 2.00 | 6.00 | 8.00 | 6.00 | 8.00 | 0.00 |
| D | 3.00 | 8.00 | 11.00 | 8.00 | 11.00 | 0.00 |
| E | 3.00 | 11.00 | 14.00 | 15.17 | 18.17 | 4.17 |
| F | 4.17 | 11.00 | 15.17 | 11.00 | 15.17 | 0.00 |
| G | 3.00 | 15.17 | 18.17 | 15.17 | 18.17 | 0.00 |
| H | 3.00 | 15.17 | 18.17 | 15.17 | 18.17 | 0.00 |
| I | 3.00 | 15.17 | 18.17 | 15.17 | 18.17 | 0.00 |
| J | 3.17 | 15.17 | 18.33 | 48.33 | 51.50 | 33.17 |
| K | 3.00 | 18.17 | 21.17 | 48.50 | 51.50 | 30.33 |
| L | 3.00 | 21.17 | 24.17 | 51.50 | 54.50 | 30.33 |
| M | 3.00 | 18.17 | 21.17 | 18.17 | 21.17 | 0.00 |
| N | 3.00 | 21.17 | 24.17 | 21.17 | 24.17 | 0.00 |
| O | 2.00 | 21.17 | 23.17 | 22.17 | 24.17 | 1.00 |
| P | 3.17 | 24.17 | 27.33 | 24.17 | 27.33 | 0.00 |
| Q | 3.00 | 27.33 | 30.33 | 27.33 | 30.33 | 0.00 |
| R | 3.00 | 30.33 | 33.33 | 30.33 | 33.33 | 0.00 |
| S | 3.00 | 27.33 | 30.33 | 30.33 | 33.33 | 3.00 |
| T | 3.00 | 33.33 | 36.33 | 33.33 | 36.33 | 0.00 |
| U | 3.00 | 36.33 | 39.33 | 36.33 | 39.33 | 0.00 |
| V | 3.00 | 8.00 | 11.00 | 40.50 | 43.50 | 32.50 |
| W | 3.00 | 11.00 | 14.00 | 43.50 | 46.50 | 32.50 |
| X | 2.00 | 14.00 | 16.00 | 79.33 | 81.33 | 65.33 |
| Y | 2.00 | 14.00 | 16.00 | 79.33 | 81.33 | 65.33 |
| Z | 3.00 | 14.00 | 17.00 | 46.50 | 49.50 | 32.50 |
| AA | 2.00 | 17.00 | 19.00 | 49.50 | 51.50 | 32.50 |
| AB | 2.00 | 17.00 | 19.00 | 49.50 | 51.50 | 32.50 |
| AC | 2.00 | 17.00 | 19.00 | 49.50 | 51.50 | 32.50 |
| AD | 3.00 | 19.00 | 22.00 | 51.50 | 54.50 | 32.50 |
| AE | 3.00 | 39.33 | 42.33 | 41.17 | 44.17 | 1.83 |
| AF | 3.00 | 39.33 | 42.33 | 39.33 | 42.33 | 0.00 |
| AG | 3.00 | 42.33 | 45.33 | 44.17 | 47.17 | 1.83 |
| AH | 3.00 | 42.33 | 45.33 | 48.33 | 51.33 | 6.00 |
| AI | 4.17 | 45.33 | 49.50 | 47.17 | 51.33 | 1.83 |
| AJ | 3.00 | 42.33 | 45.33 | 42.33 | 45.33 | 0.00 |
| AK | 3.00 | 45.33 | 48.33 | 45.33 | 48.33 | 0.00 |
| AL | 3.00 | 48.33 | 51.33 | 48.33 | 51.33 | 0.00 |
| AM | 3.17 | 51.33 | 54.50 | 51.33 | 54.50 | 0.00 |
| AN | 4.17 | 54.50 | 58.67 | 54.50 | 58.67 | 0.00 |
| AO | 3.00 | 58.67 | 61.67 | 65.00 | 68.00 | 6.33 |
| AP | 3.00 | 58.67 | 61.67 | 58.67 | 61.67 | 0.00 |
| AQ | 3.17 | 61.67 | 64.83 | 61.67 | 64.83 | 0.00 |
| AR | 3.17 | 64.83 | 68.00 | 64.83 | 68.00 | 0.00 |
| AS | 3.00 | 68.00 | 71.00 | 68.00 | 71.00 | 0.00 |
| AT | 4.17 | 71.00 | 75.17 | 71.00 | 75.17 | 0.00 |
| AU | 3.00 | 8.00 | 11.00 | 72.17 | 75.17 | 64.17 |
| AV | 3.00 | 6.00 | 9.00 | 69.17 | 72.17 | 63.17 |
| AW | 3.00 | 9.00 | 12.00 | 72.17 | 75.17 | 63.17 |
| AX | 3.00 | 62.83 | 65.83 | 72.17 | 75.17 | 9.33 |
| AY | 4.17 | 58.67 | 62.83 | 68.00 | 72.17 | 9.33 |
| AZ | 4.17 | 75.17 | 79.33 | 75.17 | 79.33 | 0.00 |
| BA | 3.00 | 75.17 | 78.17 | 76.33 | 79.33 | 1.17 |
| BB | 2.00 | 79.33 | 81.33 | 79.33 | 81.33 | 0.00 |
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