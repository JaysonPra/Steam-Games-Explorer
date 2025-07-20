# -- Color Coding for Visualizations --
COLOR_SCHEMES = {
    "price_scale": {
        "order": [
            'Free',
            '$0.01 - $4.99',
            '$5.00 - $9.99',
            '$10.00 - $19.99',
            '$20.00 - $39.99',
            '$40.00 - $59.99',
            '$60.00+'
        ],
        "colors": [
            '#99c046', # Light Steam Green - for 'Free'
            '#70b10f', # Standard Steam Green - for '$0.01 - $4.99'
            '#c6e4ee', # Very Light Steam Blue/Cyan - for '$5.00 - $9.99'
            '#66c0f4', # Standard Steam Blue - for '$10.00 - $19.99'
            '#4a789c', # Medium-Dark Steam Blue - for '$20.00 - $39.99'
            '#3b5a77', # Darker Steam Blue (Improved contrast for 40-59.99)
            '#2a475e'  # Prominent Dark Steam Blue (Improved contrast for 60+)
        ]
    },
    "indie_scale": {
        "order":[
            'Indie',
            'Non-Indie'
        ],
        "colors": [
            '#66c0f4',
            "#314961"
        ]
    }
}
