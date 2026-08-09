import dash
from dash import dcc, html
from dash.dependencies import Input, Output
import pandas as pd
import plotly.express as px


# =====================================
# LOAD DATA
# =====================================

spacex_df = pd.read_csv(r"C:\Users\MARY\Downloads\IBM-SpaceX-Capstone\Plotly Dashboard\Spacex_Launch_Dash.csv")


print(spacex_df.head())
print(spacex_df.columns)


# Convert payload to numeric
spacex_df["Payload Mass (kg)"] = pd.to_numeric(
    spacex_df["Payload Mass (kg)"],
    errors="coerce"
)


# Remove missing payload values
spacex_df.dropna(
    subset=["Payload Mass (kg)"],
    inplace=True
)


max_payload = int(
    spacex_df["Payload Mass (kg)"].max()
)


min_payload = int(
    spacex_df["Payload Mass (kg)"].min()
)



# =====================================
# CREATE DASH APP
# =====================================

app = dash.Dash(__name__)



# =====================================
# LAYOUT
# =====================================

app.layout = html.Div([


    html.H1(
        "SpaceX Launch Records Dashboard",
        style={
            "textAlign": "center",
            "color": "#503D36",
            "font-size": 40
        }
    ),



    html.Label(
        "Select Launch Site:"
    ),



    # TASK 1
    # Dropdown component

    dcc.Dropdown(

        id="site-dropdown",

        options=[

            {
                "label": "All Sites",
                "value": "ALL"
            }

        ] +

        [

            {
                "label": site,
                "value": site
            }

            for site in sorted(
                spacex_df["Launch Site"].unique()
            )

        ],

        value="ALL",

        searchable=True

    ),



    html.Br(),



    # TASK 2
    dcc.Graph(
        id="success-pie-chart"
    ),



    html.Br(),



    html.Label(
        "Payload Mass Range (Kg):"
    ),



    # TASK 3
    dcc.RangeSlider(

        id="payload-slider",

        min=0,

        max=10000,

        step=1000,

        value=[
            min_payload,
            max_payload
        ],

        marks={
            0: "0",
            2500: "2500",
            5000: "5000",
            7500: "7500",
            10000: "10000"
        }

    ),



    html.Br(),



    # TASK 4

    dcc.Graph(

        id="success-payload-scatter-chart"

    )


])



# =====================================
# TASK 2
# PIE CHART CALLBACK
# =====================================


@app.callback(

    Output(
        component_id="success-pie-chart",
        component_property="figure"
    ),

    Input(
        component_id="site-dropdown",
        component_property="value"
    )

)


def update_pie(selected_site):


    # ALL sites selected

    if selected_site == "ALL":


        success_df = spacex_df[

            spacex_df["class"] == 1

        ]


        fig = px.pie(

            success_df,

            names="Launch Site",

            title=
            "Successful Launches by Launch Site"

        )



    # Specific site selected

    else:


        site_df = spacex_df[

            spacex_df["Launch Site"] == selected_site

        ]



        fig = px.pie(

            site_df,

            names="class",

            title=
            f"Success vs Failure - {selected_site}"

        )



    return fig





# =====================================
# TASK 4
# SCATTER CALLBACK
# =====================================


@app.callback(

    Output(

        component_id=
        "success-payload-scatter-chart",

        component_property="figure"

    ),


    [

        Input(

            component_id="site-dropdown",

            component_property="value"

        ),


        Input(

            component_id="payload-slider",

            component_property="value"

        )

    ]

)


def update_scatter(selected_site, payload_range):


    low, high = payload_range



    filtered_df = spacex_df[

        (spacex_df["Payload Mass (kg)"] >= low)

        &

        (spacex_df["Payload Mass (kg)"] <= high)

    ]



    # ALL sites

    if selected_site == "ALL":


        fig = px.scatter(

            filtered_df,

            x="Payload Mass (kg)",

            y="class",

            color=
            "Booster Version Category",

            title=
            "Payload Mass vs Launch Success"

        )



    # Specific site

    else:


        site_df = filtered_df[

            filtered_df["Launch Site"]
            ==
            selected_site

        ]



        fig = px.scatter(

            site_df,

            x="Payload Mass (kg)",

            y="class",

            color=
            "Booster Version Category",

            title=
            f"Payload Mass vs Launch Success - {selected_site}"

        )


    return fig





# =====================================
# RUN APP
# =====================================

if __name__ == "__main__":

    app.run(
        debug=True
    )