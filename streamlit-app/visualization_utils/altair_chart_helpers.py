from constants.color_schemes import COLOR_SCHEMES
import altair as alt

def color_getter():
    price_scheme = COLOR_SCHEMES["price_scale"]
    color = alt.Color(
        "Price Category:N",
        title="Price Range",
        sort=price_scheme["order"],
        scale=alt.Scale(
            domain=price_scheme["order"],
            range=price_scheme["colors"]
        )
    )
    return color

def game_tooltip():
    return [
        "Name:N",
        alt.Tooltip("Release date:T", title="Release Date"),
        alt.Tooltip("AppID", title="App ID"),
        alt.Tooltip("Reviews Percentage:Q", title="Review Percentage"),
        alt.Tooltip("Price:Q", title="Price", format="$.2f"),
        alt.Tooltip("Genres:N", title="Genres")
    ]