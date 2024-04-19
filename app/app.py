# Import
import seaborn as sns
# Importing icon_svg function for displaying icons
from faicons import icon_svg
# Importing Shiny for Python
from shiny import reactive
# Importing specific components from Shiny and Shiny Express
from shiny.express import input, render, ui
# Importing the palmerpenguins dataset
import palmerpenguins 

# load the data into an initial Pandas DataFrame
df = palmerpenguins.load_penguins()

# Set up page options with a title, fillable option
ui.page_opts(title="Mhamed Penguins dashboard", fillable=True)

# A sidebar for filter controls
with ui.sidebar(title="Filter controls"):
    ui.input_slider("mass", "Mass", 2000, 6000, 6000)
    ui.input_checkbox_group(
        "species",
        "Species",
        ["Adelie", "Gentoo", "Chinstrap"],
        selected=["Adelie", "Gentoo", "Chinstrap"],
    )
    # Horizontal rule and links section with relevant URLs
    ui.hr()
    ui.h6("Links")
    ui.a(
        "GitHub Source",
        href="https://github.com/Mhamedben/cintel-07-tdash",
        target="_blank",
    )
    ui.a(
        "GitHub App",
        href="https://Mhamedben.github.io/cintel-07-tdash/",
        target="_blank",
    )
    ui.a(
        "GitHub Issues",
        href="https://github.com/Mhamedben/cintel-07-tdash/issues",
        target="_blank",
    )
    ui.a("PyShiny", href="https://shiny.posit.co/py/", target="_blank")
    ui.a(
        "Template: Basic Dashboard",
        href="https://shiny.posit.co/py/templates/dashboard/",
        target="_blank",
    )
    ui.a(
        "See also",
        href="https://github.com/denisecase/pyshiny-penguins-dashboard-express",
        target="_blank",
    )

# Creating layout columns for displaying penguin statistics
with ui.layout_column_wrap(fill=False):
    with ui.value_box(showcase=icon_svg("earlybirds"), style="font-family: Courier, monospace; font-weight: bold; color: red; background-color: yellow;"):
        ("Number of penguins")

        @render.text
        def count():
            return filtered_df().shape[0]

# Value box to display average bill length
    with ui.value_box(showcase=icon_svg("ruler-horizontal"), style="font-family: Courier, monospace; font-weight: bold; color: red; background-color: yellow;"):
        "Average bill length"

        @render.text
        def bill_length():
            return f"{filtered_df()['bill_length_mm'].mean():.1f} mm"

    # Value box to display average bill depth
    with ui.value_box(showcase=icon_svg("ruler-vertical"), style="font-family: Courier, monospace; font-weight: bold; color: red; background-color: yellow;"):
        "Average bill depth"

        @render.text
        def bill_depth():
            return f"{filtered_df()['bill_depth_mm'].mean():.1f} mm"


# Creating layout columns for displaying plots and data frames
with ui.layout_columns():
    with ui.card(full_screen=True):
        ui.card_header("Bill length and depth")

        @render.plot
        def length_depth():
            return sns.scatterplot(
                data=filtered_df(),
                x="bill_length_mm",
                y="bill_depth_mm",
                hue="species",
            )

    # Card to display summary statistics of penguin data
    with ui.card(full_screen=True):
        ui.card_header("Penguin Data")

        @render.data_frame
        def summary_statistics():
            cols = [
                "species",
                "island",
                "bill_length_mm",
                "bill_depth_mm",
                "body_mass_g",
            ]
            return render.DataGrid(filtered_df()[cols], filters=True)

#ui.include_css(app_dir / "styles.css")

# Filtered dataframe based on input values
@reactive.calc
def filtered_df():
    filt_df = df[df["species"].isin(input.species())]
    filt_df = filt_df.loc[filt_df["body_mass_g"] < input.mass()]
    return filt_df
