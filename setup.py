# Licensed under a 3-clause BSD style license - see LICENSE
from setuptools import setup

entry_points = {
    "console_scripts": [
        "vv_trend_copy_index=vv_trend.copy_index:main",
        "vv_trend_update_plots=vv_trend.vv_trend:main",
    ]
}

setup(
    name="vv_trend",
    author="Jean Connelly",
    description="Update aspect pipeline centroid residual plots",
    author_email="jconnelly@cfa.harvard.edu",
    use_scm_version=True,
    setup_requires=["setuptools_scm", "setuptools_scm_git_archive"],
    zip_safe=False,
    license=(
        "New BSD/3-clause BSD License\nCopyright (c) 2019"
        " Smithsonian Astrophysical Observatory\nAll rights reserved."
    ),
    entry_points=entry_points,
    packages=["vv_trend"],
    package_data={"vv_trend": ["data/index_template.html", "task_schedule.cfg"]},
)
