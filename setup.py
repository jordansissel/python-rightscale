from distutils.core import setup

setup(name="rightscale",
      version="0.200",
      description="Object-oriented model for RightScale's REST API",
      author="Jordan Sissel",
      author_email="jordan@loggly.com",
      url="none-yet",
      packages=["rightscale", "rightscale.util"],
      package_dir = { 
        "rightscale": "src/rightscale",
        "rightscale.": "src/rightscale/util",
      },
      requires=["httplib2", "netifaces"],
      )

