from setuptools import find_packages, setup

setup(
    name="blackjack",
    version="1.0",
    description="Blackjackで遊ぶ",
    author="ykskks",
    # author_email='',
    url="https://github.com/ykskks/blackjack",
    packages=find_packages(),
    entry_points="""
      [console_scripts]
      bj = blackjack.cli:execute
    """,
)
