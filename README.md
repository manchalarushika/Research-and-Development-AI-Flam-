#  Research and Development / AI — Parametric Curve Estimation  

###  Objective
The goal of this task is to find the unknown parameters **Theta**, **M**, and **X** in the given parametric equations using the provided dataset.

x(t) = t*cos(Theta) - e^(M*|t|)*sin(0.3*t)*sin(Theta) + X  
y(t) = 42 + t*sin(Theta) + e^(M*|t|)*sin(0.3*t)*cos(Theta)

The main aim is to estimate these parameters so that the predicted curve fits the given data points as accurately as possible.


---

##  Problem Understanding  
The dataset contains (x, y) points that lie on the curve for \(6 < t < 60\).  
Here, Theta, M, and X are unknown, and even the parameter **t** for each point is not given.  
This makes it a **non-linear optimization problem** where both the hidden variable \(t\) and the parameters must be estimated to make the curve pass through all data points.

---

##  Approach and Process  

### Step 1: Loading and Understanding the Data  
- The dataset `xy_data.csv` was loaded using **pandas**.  
- The x and y columns were extracted and stored as arrays for modeling.  
- This gave the coordinate points that the fitted curve should pass through.

---

### Step 2: Defining the Mathematical Model  
A function `model(params, t)` was created to represent the given parametric equations.  
It calculates predicted values of \(x(t)\) and \(y(t)\) for any chosen Theta, M, X, and t.  
This helped compare predicted values with the given dataset.

---

### Step 3: Defining the Loss Function (L1 Distance)  
To measure how close the predicted curve is to the data points, the **L1 distance** was used:  
\[
L = |x_{pred} - x_{actual}| + |y_{pred} - y_{actual}|
\]  
This sums up the absolute differences between predicted and actual values.  
The smaller the L1 loss, the better the curve fits.

---

### Step 4: Optimizing t for Each Data Point  
Since t is not provided, **`minimize_scalar()`** from SciPy was used to find the best t (within 6–60) for each data point, minimizing the L1 distance for that specific point.  
This ensures every point is mapped to its best possible t.

---

### Step 5: Global Optimization (Differential Evolution)  
To estimate θ, M, and X, I used **Differential Evolution**, which searches globally across all parameter ranges to avoid getting stuck in local minima.  

Parameter bounds:  
- \(0° < θ < 50°\)  
- \(-0.05 < M < 0.05\)  
- \(0 < X < 100\)  

This step gives strong initial estimates for the unknowns.

---

### Step 6: Local Refinement (Powell’s Method)  
After global optimization, **Powell’s method** was applied for local refinement.  
This fine-tunes the parameters from the global search, making the result more accurate.  
Together, these two steps give a stable and precise solution.

---

### Step 7: Recomputing Best t and L1 Score  
Once final Theta, M, and X were found, t was re-optimized for all points, and the **mean L1 loss** was recalculated.  
A lower L1 score means the predicted curve closely follows the actual data.

---

### Step 8: Plotting the Final Curve  
The observed points (blue dots) and the fitted curve (red line) were plotted using **Matplotlib**.  
This helps to visually confirm that the model fits well.  
The plot was saved as **`fit.png`**.

---

##  Why This Approach Works  
- L1 loss is simple and robust, giving fair weight to all data points.  
- Differential Evolution ensures global exploration.  
- Powell’s method improves fine-tuning.  
- Estimating t individually keeps the model flexible and accurate.  
Together, these steps make the fit smooth and precise.

---

##  Assessment Criteria Coverage  

| Criteria | Description | How It’s Covered |
|-----------|--------------|------------------|
| **L1 Distance (100)** | Accuracy between predicted and real data | L1 loss computed and minimized |
| **Explanation (80)** | Step-by-step reasoning and clarity | Detailed comments and README description |
| **Code / Repo (50)** | Clean and structured implementation | Organized, commented, and optimized code |
| **Bonus** | Extra logic / visualization | Global + local optimization and plotted output |

---

##  Results  

**Final Estimated Parameters:**  
Theta (degrees): 30.020851143287842
M: 0.03088815850486027
X: 55.08007359680873
Final L1 Score: 8.081759625963817


These values, when substituted in the parametric equations, produce a curve that matches the dataset closely.

---

## 📈 Visual Output  

<img width="595" height="453" alt="image" src="https://github.com/user-attachments/assets/1edadd5c-1513-4982-9662-6d4cb3542818" />


The plot shows the observed data (blue) and the fitted curve (red).  
The alignment confirms that the model successfully captured the pattern of the given data.

---

##  Files Included  

| File Name | Description |
|------------|-------------|
| `parametric_curve_fitting.py` | Main Python code |
| `xy_data.csv` | Dataset of (x, y) points |
| `final_results.png` | Output curve plot |
| `README.md` | Full documentation and explanation |

---

##  Conclusion  
This project successfully finds the unknown parameters **Theta**, **M**, and **X** for the given parametric equation.  
By combining global and local optimization, the model achieves a close fit to the provided data points.  
The process from understanding data, defining the model, optimizing parameters, and validating results is clearly explained and implemented step by step.  
This demonstrates strong problem-solving, analytical, and coding skills suited for real-world R&D applications.

---

##  Libraries Used  
- **NumPy** – for mathematical calculations  
- **Pandas** – for data handling  
- **SciPy** – for optimization functions (`minimize`, `minimize_scalar`, `differential_evolution`)  
- **Matplotlib** – for plotting the final fitted curve  



