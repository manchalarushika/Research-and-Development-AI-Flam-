
# # Importing required Libraries
import numpy as np # for Mathamatical calculations
import pandas as pd # for reading the dataset
from scipy.optimize import minimize, minimize_scalar, differential_evolution # for performing the optimization (to find best parameter values)
import matplotlib.pyplot as plt # for plotting graphs and comparing fitted and real data visually


# # Loading the dataset
df=pd.read_csv("xy_data.csv")
x_data=df["x"].values
y_data=df["y"].values
N=len(x_data)
# I loaded the CSV file that contains the given data points (x, y).
# Then I separated the values of x and y into arrays and stored the total number of points in N.


# # Defining the given parametric equations
def model(params,t):
    theta,M,X=params
    x_pred=t*np.cos(theta)-np.exp(M*np.abs(t))*np.sin(0.3*t)*np.sin(theta)+X
    y_pred=42+t*np.sin(theta)+np.exp(M*np.abs(t))*np.sin(0.3*t)*np.cos(theta)
    return x_pred,y_pred
# This function represents the mathematical equations given in the question.
# It calculates x and y based on the parameters theta, M, and X, and for a particular t value.


# # Calculating loss for one point  
def point_loss_for_params(params,idx):
    xi,yi=x_data[idx],y_data[idx]
    res=minimize_scalar(
        lambda ti:np.abs(model(params,ti)[0]-xi)+np.abs(model(params,ti)[1]-yi),
        bounds=(6,60),
        method="bounded",
        options={"xatol":1e-2,"maxiter":80},
    )
    best_t=res.x
    x_pred,y_pred=model(params,best_t)
    return np.abs(x_pred-xi)+np.abs(y_pred-yi)
# For each data point, I don’t know the exact t value.
# So here I used minimize_scalar() to find the best t between 6 and 60 that minimizes the L1 distance (|x_pred-x| + |y_pred-y|).
# This function returns the total error for that one data point.


# # Calculating total L1 loss
subset_indices=np.linspace(0,N-1,min(100,N),dtype=int)
def total_loss(params,use_subset=False):
    indices=subset_indices if use_subset else range(N)
    return sum(point_loss_for_params(params,i) for i in indices)
# To evaluate how good the parameters are, I summed up the individual losses for all points.
# For faster global search, I sometimes use only 100 sample points (subset_indices),and for final refinement,I use all data points.


# # Global optimization (Differential Evolution)
bounds=[(np.deg2rad(0),np.deg2rad(50)),(-0.05, 0.05),(0, 100)]
result_global=differential_evolution(
    lambda p:total_loss(p,use_subset=True),
    bounds,
    maxiter=20,
    popsize=10,
    polish=False,
    seed=0,
)
# Here I used Differential Evolution, a global optimization algorithm.
# It tries different combinations of theta , M, and X across the given range and finds a good starting point for them.
# This avoids getting stuck in local minima


# # Local optimization
result_local=minimize(lambda p:total_loss(p,use_subset=False),result_global.x,bounds=bounds,method="Powell")
theta,M,X=result_local.x
# After getting the rough global values, I refined them using Powell’s method for more accuracy on the full dataset.
# This gives the final optimized values of theta, M, and X.


# # Finding best t values for each data point
t_opt=np.zeros(N)
for i in range(N):
    res=minimize_scalar(
        lambda ti:np.abs(model([theta,M,X],ti)[0]-x_data[i])+np.abs(model([theta,M,X],ti)[1]-y_data[i]),
        bounds=(6,60),
        method="bounded",
        options={"xatol":1e-2,"maxiter":80},
    )
    t_opt[i]=res.x
# Once theta,M,and X are known,I again found the best t for every data point individually so that the curve fits as closely as possible.


# # Calculating final score
x_pred,y_pred model([theta,M,X],t_opt)
L1_score=np.mean(np.abs(x_pred-x_data)+np.abs(y_pred-y_data))
# This computes the average L1 error between predicted and actual points  this is the score used to measure accuracy.


# # Displaying the results
print(f"Theta (degrees):{np.degrees(theta)}")
print(f"M:{M}")
print(f"X:{X}")
print(f"Final L1 Score:{L1_score}")
# I printed the final parameter values and the calculated L1 distance to see how well the curve fits.


# # Creating the submission string
final_equation=f"(t*cos({theta})-e^({M}|t|)*sin(0.3t)*sin({theta})+{X},42+t*sin({theta})+e^({M}|t|)*sin(0.3t)*cos({theta}))"
print(final_equation)


# # Plotting the curve
plt.figure(figsize=(8,6))
plt.scatter(x_data,y_data,label="Observed Data",s=10)
plt.plot(x_pred,y_pred,'r-',label="Fitted Curve")
plt.xlabel("x")
plt.ylabel("y")
plt.legend()
plt.title("Final Curve Fit")
plt.grid(True)
plt.savefig("fit.png",dpi=150)
plt.show()
# Finally,I plotted the original data points (blue dots) and the fitted curve (red line) to visually confirm that the model fits correctly.
# The plot is saved as fit.png






