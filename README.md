# manipulator

1. Install Docker Engine (not Docker Desktop, they are different
in ways that will complicate this setup from working as 
expected)
  - https://docs.docker.com/engine/install/ubuntu/
  
on your host system run the following commands:
```
curl -fsSL https://get.docker.com -o get-docker.sh
sudo sh get-docker.sh
sudo usermod -aG docker $USER
sudo systemctl enable docker.service
sudo systemctl enable containerd.service
reboot
```

## Add permission for docker to access display

Run this in a terminal on your host system
```
xhost +local:docker
```


## Start up ROS1

```
docker compose --file docker-compose.ros1-dev.yaml up
```

Access the terminal within the docker environment


```
docker exec -it ros1-dev bash
```


# Planning Pipelines

There are about four planning pipelines that I have used in my project. They are called OMPL, STOMP, CHOMP, and PILZ. In this document, we'll be exploring the advantages of each pipeline and explore the similarities and differences.

## OMPL
The Open Motion Planning Library is a powerful collection of state-of-the-art sampling-based motion planning algorithms and is the default planner in MoveIt.

* Many planners in OMPL (including the default one) favor speed of finding a solution path over path quality.
* A feasible path is smoothened and shortened in a post-processing stage to obtain a path that is closer to optimal. 
* However, there is no guarantee that a global optimum is found or that the same solution is found each time since the algorithms in OMPL are probabilistic. 
* The planners in OMPL typically terminate when a given time limit has been exceeded.
* A solution would be eventually found if one exists, however non-existence of a solution cannot be reported.
* These algorithms are efficient and usually find a solution quickly
* OMPL does not contain any code related to collision checking or visualization as the designers of OMPL did not want to tie it to a any particular collision checker or visualization front end.
* MoveIt integrates directly with OMPL and uses the motion planners from OMPL as its default set of planners. 
* The planners in OMPL are abstract; i.e. OMPL has no concept of a robot. Instead, MoveIt configures OMPL and provides the back-end for OMPL to work with problems in Robotics

There are several planners in OMPL that can give theoretical optimality guarantees, which are typically the minimization of path length. Here are some examples:
* RRT*, PRM*, LazyPRM*, BFMT, FMT, Lower Bound Tree RRT (LBTRRT), SPARS, SPARS2, Transition-based RRT (T-RRT)

However, other optimization objectives can be used as well such as:
* PathLengthOptimizationObjective (Default)
* MechanicalWorkOptimizationObjective
* MaximizeMinClearanceObjective
* StateCostIntegralObjective
* MinimaxObjective

OMPL also provides a meta-optimization algorithm called AnytimePathShortening, which repeatedly runs several planners in parallel with path shortcutting and path hybridization to locally optimize a solution path.

## CHOMP

CHOMP is a gradient-based trajectory optimization procedure that makes many everyday motion planning problems both simple and trainable.

* This algorithm is capable of reacting to the surrounding environment to quickly pull the trajectory out of collision while simultaneously optimizing dynamical quantities such as joint velocities and accelerations. 
* It rapidly converges to a smooth collision-free trajectory that can be executed efficiently on the robot.
* This pipeline designs a motion planning algorithm based entirely on trajectory optimization instead of separating trajectory generation into distinct planning and optimization stages.
* For scenes containing obstacles, CHOMP often generates paths which do not prefer smooth trajectories by addition of some noise (ridge_factor) in the cost function for the dynamical quantities of the robot (like acceleration, velocity). 
* OMPL can be used to generate collision-free seed trajectories for CHOMP to mitigate this issue.

## STOMP

STOMP produces smooth well behaved collision free paths within reasonable times. The approach relies on generating noisy trajectories to explore the space around an initial (possibly infeasible) trajectory which are then combined to produce an updated trajectory with lower cost.

 Some of the moveIt planners tend to produce jerky trajectories and may introduce unnecessary robot movements. A post processing smoothing step is usually needed.
 * STOMP tends to produce smooth well behaved motion plans in a short time, there is no need for a post processing smoothing step as required by some other motion planners.
 * CHOMP optimizes a given initial naive trajectory based on convarient and functional gradient approaches. CHOMP is entirely based on trajectory optimization.
 * OMPL is an open source library for sampling based / randomized motion planning algorithms. A solution would be eventually found if one exists, however non-existence of a solution cannot be reported.

### Comparisons

Local Minima Handling
* STOMP can avoid local minima due to its stochastic nature. 
* CHOMP however is prone to and gets often stuck in local minima, thereby avoiding an optimal solution or returns sub-optimal solutions. 
* STOMP performs better.

Time Requirements
* The execution times are comparable, even though CHOMP requires more iterations to achieve success than STOMP.
* OMPL algorithms are efficient and usually find a solution quickly.

Parameter Tuning
* CHOMP generally requires additional parameter tuning than STOMP to obtain a successful solution. 
* OMPL does not require a lot of parameter tuning, the default parameters do a good job in most situations.

Obstacle Handling
* STOMP often is able to successfully avoid obstacles due to its stochastic nature
* CHOMP however generates paths which do not prefer smooth trajectories by addition of some noise (ridge_factor) in the cost function for the dynamical quantities of the robot (like acceleration, velocity).
* OMPL also generates collision free smooth paths in the presence of obstacles.

# PILZ Industrial Motion Planner

This pipeline provides a trajectory generator to plan standard robot motions like PTP, LIN, CIRC with the interface of a MoveIt PlannerManager plugin.
* Note, that these planners are motion generators only, i.e. they don’t consider obstacle avoidance. 
* The intended trajectory (LINear or CIRCular in Cartesian space, or PTP) is computed and only finally tested for validity regarding collisions. 
* If a collision occurs, the whole trajectory is rejected.


