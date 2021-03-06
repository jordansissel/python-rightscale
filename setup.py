from distutils.core import setup

setup(name="rightscale",
      version="0.309",
      description="Object-oriented library for RightScale's API.",
      author="Jordan Sissel",
      author_email="jordan@loggly.com",
      url="none-yet",
      packages=["rightscale", "rightscale.util"],
      package_dir = { 
        "rightscale": "src/rightscale",
        "rightscale.util": "src/rightscale/util",
      },
      requires=["httplib2", "netifaces"],
      )

