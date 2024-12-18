import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
from sklearn.preprocessing import PolynomialFeatures
from sklearn.pipeline import make_pipeline

def generate_data():
    np.random.seed(42)
    X = np.sort(np.random.rand(100, 1) * 10, axis=0)
    y = np.sin(X).ravel() + np.random.normal(0, 0.1, X.shape[0])
    return X, y

def create_animation():
    X, y = generate_data()
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=0)

    fig, axes = plt.subplots(1, 2, figsize=(12, 6))
    axes[0].set_xlim((0, 10))
    axes[0].set_ylim((-2, 2))
    axes[0].set_title('Training Data')
    axes[1].set_xlim((0, 10))
    axes[1].set_ylim((-2, 2))
    axes[1].set_title('Validation Data')

    line_train, = axes[0].plot([], [], 'o', label='Training data')
    line_model_train, = axes[0].plot([], [], '-', label='Model on Training data')
    line_test, = axes[1].plot([], [], 'o', label='Validation data')
    line_model_test, = axes[1].plot([], [], '-', label='Model on Validation data')

    step_text = axes[0].text(0.02, 0.95, '', transform=axes[0].transAxes)
    degree_text = axes[1].text(0.02, 0.95, '', transform=axes[1].transAxes)

    for ax in axes:
        ax.legend()

    def init():
        line_train.set_data([], [])
        line_model_train.set_data([], [])
        line_test.set_data([], [])
        line_model_test.set_data([], [])
        degree_text.set_text('')
        return line_train, line_model_train, line_test, line_model_test, step_text, degree_text

    def update(degree, step):
        model = make_pipeline(PolynomialFeatures(degree), LinearRegression())
        model.fit(X_train[:step], y_train[:step])
        X_fit = np.linspace(0, 10, 100).reshape(-1, 1)
        y_fit_train = model.predict(X_fit)
        y_fit_test = model.predict(X_test)
        
        line_train.set_data(X_train[:step], y_train[:step])
        line_model_train.set_data(X_fit, y_fit_train)
        line_test.set_data(X_test, y_test)
        line_model_test.set_data(X_test, y_fit_test)
        step_text.set_text(f'Step: {step}')
        degree_text.set_text(f'Degree: {degree}')
        return line_train, line_model_train, line_test, line_model_test, step_text, degree_text

    ani = animation.FuncAnimation(fig, update, frames=range(1, len(X_train)+1), fargs=(len(X_train),), init_func=init, blit=True, repeat=False)
    plt.show()

if __name__ == "__main__":
    create_animation()