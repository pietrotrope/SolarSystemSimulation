AU = (149.6e6 * 1000)

data = {
    "Saturn": {
        "mass": 5.6834 * 10**26,
        "radius": 20,
        "initialPosition": [10.539*AU, AU, 0.1],
        "initialVelocity": [0.0, - 9.68 * 1000, 0.0],
        "color": (120, 80, 80)
    },

    "Jupiter": {
        "mass": 1.8982 * 10**27,
        "radius": 20,
        "initialPosition": [6.203*AU, AU, 0.1],
        "initialVelocity": [0.0, - 13.07 * 1000, 0.0],
        "color": (135, 94, 19)
    },

    "Mars": {
        "mass": 6.4171 * 10**23,
        "radius": 12,
        "initialPosition": [2.524*AU, AU, 0.1],
        "initialVelocity": [0.0, - 24.077 * 1000, 0.0],
        "color": (255, 30, 30)
    },

    "Earth": {
        "mass": 5.97237 * 10**24,
        "radius": 14,
        "initialPosition": [2*AU, AU, 0.1],
        "initialVelocity": [0.0, - 29.783 * 1000, 0.00],
        "color": (102, 255, 255)
    },

    "Moon": {
        "mass": 7.342 * 10**22,
        "radius": 5,
        "initialPosition": [(2 + 0.002569)*AU, AU, 0.1],
        "initialVelocity": [0.0, (-1.022 - 29.783)*1000, 0.00],
        "color": (255, 255, 255)
    },

    "Venus": {
        "mass": 4.8685 * 10**24,
        "radius": 8,
        "initialPosition": [1.723*AU, AU, 0.1],
        "initialVelocity": [0.0, -35.02 * 1000, 0.0],
        "color": (255, 130, 130)
    },

    "Mercury": {
        "mass": 3.3011*10**23,
        "radius": 10,
        "initialPosition": [1.39*AU, AU, 0.1],
        "initialVelocity": [0.0, - 47.36 * 1000, 0.0],
        "color": (160, 160, 160)
    },

    "Sun": {
        "mass": 1.9885 * 10**30,
        "radius": 24,
        "initialPosition": [AU, AU, 0.1],
        "initialVelocity": [0.0, 0.0, 0.0],
        "color": (255, 255, 0)
    }
}
