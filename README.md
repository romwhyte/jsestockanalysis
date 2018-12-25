# JSE Stock Analysis

The goal of this project of mine is to bring users to try and experiment with the stock analysis calculation to gain investment insight. 

## How to use this ".ipynb" Python notebook ?

Except the fact I made available an ".py" Python version of this tutorial within the repository, it is more convenient to run the code inside the notebook. The ".py" code exported feels a bit raw as an exportation.

To run the notebook, you must have installed Jupyter Notebook or iPython Notebook. To open the notebook, you must write `jupyter notebook` or `iPython notebook` in command line (from the folder containing the notebook once downloaded, or a parent folder). It is then that the notebook application (IDE) will open in your browser as a local server and it will be possible to open the `.ipynb` notebook file and to run code cells with `CTRL+ENTER` and `SHIFT+ENTER`, it is also possible to restart the kernel and run all cells at once with the menus. Note that this is interesting since it is possible to make that IDE run as hosted on a cloud server with a lot of GPU power while you code through the browser.

## Cleaning Data

Note that the dataset will be updated daily and stock variables can be changed to display different stock results 

## Stock Analysis

In theory, it is possible to create a perfect prediction of the signal for this exercise. The neural network's parameters has been set to acceptable values for a first training, so you may pass this exercise by running the code without even a change. Your first training might get predictions like that (in yellow), but it is possible to do a lot better with proper parameters adjustments:


### Portfolio Analysis

This analysis allows multiple stock to be valuated.  The calculation utilize the effeciency fontier, 




## Author

Romayne Whyte
- https://ca.linkedin.com/in/romwhyte
- https://github.com/romwhyte/

## License

This project is free to use according to the [MIT License](https://github.com/romwhyte/jsestockanalysis/blob/master/LICENSE) as long as you cite me and the License (read the License for more details). You can cite me by pointing to the following link:
- https://github.com/romwhyte/jsestockanalysis

## Converting notebook to a readme file

```python
# Let's convert this notebook to a README for the GitHub project's title page:
!jupyter nbconvert --to markdown stock analysis.ipynb
!mv stock analysis.md README.md
```