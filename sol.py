import solara
import solara.lab

import reacton.ipyvuetify as rv

# import sympy as sp
import pandas as pd
import numpy as np
# import matplotlib.pyplot as plt
# from matplotlib.ticker import MultipleLocator, FormatStrFormatter
# from matplotlib.ticker import FormatStrFormatter

from matplotlib.figure import Figure

# plt.switch_backend('Agg')


@solara.component
def Radio(label, value, values, on_value):
    value_ = solara.use_reactive(value, on_value)
    del value, on_value
    with rv.RadioGroup(label=label, v_model=value_.value, on_v_model=value_.set):
        for _value in values:
            rv.Radio(label=_value, value=_value)


REGIONS = ["Africa",
           "$x^2$",
           "Asia",
           "Europe",
           "Oceania",
           "All"]

# @solara.component
# def Page():


data = pd.read_csv("life-expectancy_US_Worlds.csv",
                   index_col=0).drop(columns=['World'])

x_data = data.index[:].to_list()
y_data = data.iloc[0:, 0].to_list()


def linear_function(x, m, b):
    return m * x + b


def plot_data(slope: float, intercept: float):
    x = np.linspace(0, 150, 150)
    y = linear_function(x, slope, intercept)
    # fig = plt.figure(figsize=(8, 6))

    DP = 2

    fig = plt.figure(figsize=(8, 6), dpi=100, facecolor='w', edgecolor='k')
    fig.canvas.draw()
    ax = plt.gca()

    # set up axis
    ax.spines['left'].set_position('zero')
    ax.spines['right'].set_color('none')
    ax.spines['bottom'].set_position('zero')
    ax.spines['top'].set_color('none')
    ax.xaxis.set_ticks_position('bottom')
    ax.yaxis.set_ticks_position('left')

    # draw curve
    ax.plot(x, y)

    # line, = ax.plot(x, y)
    ax.scatter(range(1, len(y_data) + 1), y_data, c=["red"], s=2)

    # mark point
    # ax.plot(x[129], y[129] , 'ro')

    # set bounds
    ax.set_xbound(0, 150)
    ax.set_ybound(0, 100)

    # format axes and grid
    ax.xaxis.set_major_locator(MultipleLocator(10))
    ax.yaxis.set_major_locator(MultipleLocator(10))
    ax.xaxis.grid(True, 'major', linewidth=2 / DP,
                  linestyle='-', color='#d7d7d7', zorder=0)
    ax.yaxis.grid(True, 'major', linewidth=2 / DP,
                  linestyle='-', color='#d7d7d7')

    ax.xaxis.set_minor_locator(MultipleLocator(2))
    ax.yaxis.set_minor_locator(MultipleLocator(2))
    ax.xaxis.grid(True, 'minor', linewidth=0.5 / DP,
                  linestyle='-', color='#d7d7d7')
    ax.yaxis.grid(True, 'minor', linewidth=0.5 / DP,
                  linestyle='-', color='#d7d7d7')

    ax.set_axisbelow(True)
    ax.set_aspect('equal')

    # plt.show(fig)

    # plt.plot(x, y)
    #
    # plt.xlim(0, 122)
    # plt.ylim(0, 100)
    # plt.xlabel('x')
    # plt.ylabel('y')

    return fig


# Declare reactive variables at the top level. Components using these variables
# will be re-executed when their values change.
sentence = solara.reactive("Solara makes our team more productive.")
word_limit = solara.reactive(10)
slope = solara.reactive(0.15)
intercept = solara.reactive(40.0)

model = solara.reactive("")

show_message = solara.reactive(False)
solution_message = solara.reactive("Show Answer")


@solara.component
def Page():

    solara.Title("Modeling data with linear functions")

    with solara.AppBarTitle():
        solara.Text("Modeling data with linear functions")

    # with solara.Sidebar():
    #     solara.Markdown("")
    #     # solara.SliderInt(label="Ideal for placing controls")

    with solara.Column():

        # with solara.Card():
        solara.Markdown("""
        # Modeling data with linear functions
                        
        The graph below shows average US life expectancy for every year between 1901
        and 2021 (the red dots). The $x$-axis corresponds to year $1900+x$.

        Looking at the red dots, you notice that they **follow a linear trend**: with
        a few exceptions, the points closely follow a straight line. 

        (What are the exceptions (*outliers*) and how would you explain them? In other
        words, what happened in the US in 1918 and in 2020-21 that had a negative
        impact on life expectancy?)
        """)

        with solara.Columns([1, 1]):
            with solara.Card(title="Linear Model"):
                # Calculate word_count within the component to ensure re-execution when reactive variables change.
                # word_count = len(sentence.value.split())

                # solara.InputText(label="Your sentence", value=sentence,
                #                  continuous_update=True)
                solara.SliderFloat("Slope", value=slope,
                                   step=0.001, min=0.15, max=0.40)
                solara.SliderFloat("Intercept", value=intercept,
                                   min=40.0, max=65.0)

                solara.Markdown(
                    f"Your model: $y = {slope}\cdot x + {intercept}$")

                freq, set_freq = solara.use_state(2.0)

                x = np.linspace(0, 150, 150)
                y = linear_function(x, slope.value, intercept.value)

                fig = Figure()
                ax = fig.subplots()
                ax.scatter(range(1, len(y_data) + 1), y_data, c=["red"], s=2)
                ax.plot(x, y)
                ax.set_ylim(0, 100)
                ax.set_xlim(0, 150)

                solara.FigureMatplotlib(
                    fig, dependencies=[slope.value, intercept.value])

            with solara.lab.Tabs():

                with solara.lab.Tab("Interpreting the model"):
                    solara.Markdown("""
                        The blue line represents a linear function, determined by its **slope** and its **y-intercept**, that **models the data**.
                        """)

                    solara.Markdown(
                        f"Your model: $${slope} \cdot x + {intercept}$$")

                    solara.Markdown("""
                        Mathematically, the model is simply a linear function defined by slope and intercept. But since it is 
                        supposed to model data, slope and intercept have practical interpretations. Answer the questions below to 
                        test your understanding.
                        """)

                with solara.lab.Tab("Applying the model"):
                    solara.Markdown(f"We want to use our model \
                        $${slope} \cdot x + {intercept}$$ \
                        to make predictions about the future average life expectancy of the US population.")

                    solara.Markdown("""
                        #### Estimating future life expectancy
                        
                        For example, we would like to estimate the average life expectancy in 2030.
                        For this purpose, we use the value of our model at $x=130$
                        (keep in mind that $x=0$ corresponds to the year 1900).
                        
                        You can compute this value or try to read it off the graph. 
                        """)

                    # solara.Select(label="Food", value="abab",
                    #               values=["abab", "cdcd"], disabled=True)

                    # region, set_region = solara.use_state("Asia")
                    # Radio(label="Select A Region", value=region,
                    #       on_value=set_region, values=REGIONS)
                    # solara.Markdown(f"current region is {region}")

                    solara.Switch(label=solution_message.value,
                                  value=show_message)

                    if show_message.value:
                        solara.Markdown(f"""
                            Estimated US life expectancy in 2030: \
                                        ${round(linear_function(130, slope.value, intercept.value),2)}$ years 
                            """)

                    # with rv.ExpansionPanels(v_model=target, on_v_model=set_target, mandatory=False, value=open):
                    #     with rv.ExpansionPanel():
                    #         rv.ExpansionPanelHeader(
                    #             children=["Jupyter notebook"])
                    #         with rv.ExpansionPanelContent():
                    #             solara.Markdown(
                    #                 "Build on top of ipywidgets, solara components work in all Jupyter notebook environments.")

                    # with solara.Row():
                    #     solara.Button(label="(1)", outlined=True)
                    #     solara.Markdown("The choice $x_1$")
                    # with solara.Row():
                    #     solara.Button(label="(2)", outlined=True)
                    #     solara.Markdown("The choice $x_1$")
                    # with solara.Row():
                    #     solara.Button(label="(3)", outlined=True)
                    #     solara.Markdown("The choice $x_1$")
                    # with solara.Row():
                    #     solara.Button(label="(4)", outlined=True)
                    #     solara.Markdown("The choice $x_1$")
#         with st.expander("Estimated US life expectancy in 2030:"):
#             st.write(
#                 str(round(linear_function(130, user_slope, user_intercept), 2)) + " years")

#         """
#         **According to the model, what is the estimated US life expectancy in 2040?**
# ")


# # The following line is required only when running the code in a Jupyter notebook:
# Page()
