# Python-based darts recording web application
App for recording darts practice and analysing data. Available pages are:
- Match: two player darts match from 301 or 501. See [screenshot](./assets/screenshots/match.png).
- Practice: T20, T19 and Bull practice modes. See [T20/T19 screenshot](./assets/screenshots/t20.jpg), [Bull screenshot](./assets/screenshots/bull.png)
- TODO: plotting and analysis pages

## T20 and T19 practice modes
These pages can be used during practice (exclusively aiming at T20/T19) and each of the three darts is recorded using the numpad (1-20, 25, Bull and Miss). These darts are saved, after pressing the confirm button, to a `t20_practice.csv` (or `t19_practice.csv`) file in the project folder.

On the page, the user can see the 3-dart average of their current session (reverts to 0 upon refresh), and the 3-dart average of all time (calculated from the saved darts in the .csv file).

## Bullseye practice mode
This page is slightly different than the T20 and T19 practice pages, hence is defined in a separate file: `bull_practice.py`. This is because we are not necessarily aiming to maximise score when aiming for Bull. Instead, this page just keeps track of the number of total hits of 25 and Bull during the current session (reverts to 0 upon refresh) and of all time (calculated from the `bull_practice.csv` file in the project directory).

## Plot example (not yet integrated into app functionality)
This plot is a plot of the frequency of the scores and the scores as they appear on the board, linearised onto the x-axis. The data is stored in the .csv files and Pandas is used to extract the relevant dart frequencies. These plots can reveal interesting phenomena, for example, I appear to hit 5 much more frequently than 1 when aiming for T20, suggesting I have a systematic left bias present in the mechanics of my throw.<br>
![score_freq_dart_all_sngl_dbl_tbl](https://github.com/Henryp1997/darts_app/assets/118852495/015b932b-f1c7-4d5e-b8c9-5e2dd001a149)
