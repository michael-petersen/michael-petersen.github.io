
# try this search as a jumping off place for collecting bibcodes
# https://ui.adsabs.harvard.edu/search/p_=0&q=author%3A%22Petersen%2C%20Michael%20S.%22&sort=date%20desc%2C%20bibcode%20desc

def get_first_author_bibcodes():
    # First author bibcodes
    return [
        "2016MNRAS.463.1952P",
        "2016PhRvD..94l3013P",
        "2019MNRAS.488.1462P",
        "2019MNRAS.490.3616P",
        "2020MNRAS.494L..11P",
        "2021MNRAS.500..838P",
        "2021NatAs...5..251P",
        "2022MNRAS.510.6201P",
        "2022MNRAS.514.1266P",
        "2024MNRAS.530.4378P",
        "2024MNRAS.531..751P",
        "2025JOSS...10.7302P",
        "2019arXiv190308203P" # this is the paper that was never published
        ]

def get_student_led_bibcodes():
    return [
        "2022MNRAS.512..160R",
        "2022MNRAS.513L..46D",
        "2023MNRAS.518..774L",
        "2023MNRAS.521.1757J",
        "2024MNRAS.531.3524Y",
        "2025JOSS...10.7009S", # commensurability
        "2025MNRAS.539..661G" # flex
        ]

def get_coauthor_bibcodes():
    return [
        "2014ApJ...792...64B",
        "2021MNRAS.501.5408W",
        "2021MNRAS.508L..26P",
        "2025MNRAS.538..998H",
        "2024JOSS....9.6906N", # lintsampler
        "2025arXiv250609927F", # retrograde stars
        ]

def get_collaborative_bibcodes():
    # collaborative bibcodes
    return [
        "2009ApJ...701..306E",
        "2023ApJ...942...18C",
        "2023MNRAS.518.4138E",
        "2023ApJ...946...10P",
        "2023MNRAS.520.4779L",
        "2024MNRAS.532.2657B",
        "2024arXiv241215033T",
        "2025arXiv250104095Y",
        "2025A&A...697A.214B", # dark matter spirals
        "2025arXiv250420133A", # mssa on fire
        "2025arXiv250613636T" # krios paper
        ]