import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd
from DB.dbHelperMethods import searchForUserValuations


def startBuildingValuationsCharts(userId):
    valuation = searchForUserValuations(userId)
    df = pd.DataFrame({'AssetsOrLiability': ["Assets", "Liabilities"],
                       'Property Values': [valuation.propertyValuesAsset, 0.00],
                       'Savings Accounts': [valuation.savingsAccountsAsset, 0.00],
                       'Pensions Accounts': [valuation.pensionsAccountsAsset, 0.00],
                       'Cars': [valuation.carsAsset, 0.00],
                       'Other Assets': [valuation.otherAsset, 0.00],
                       'Mortgages': [0.00, valuation.mortgagesLiability],
                       'Student Loans': [0.00, valuation.studentLoanLiability],
                       'Personal Loans': [0.00, valuation.personalLoanLiability],
                       'Car Loans': [0.00, valuation.carLoansLiability],
                       'Other Debt': [0.00, valuation.otherDebtLiability]
                       })
    buildBarChart(df)

    assets = [valuation.propertyValuesAsset, valuation.savingsAccountsAsset, valuation.pensionsAccountsAsset,
              valuation.carsAsset, valuation.otherAsset]
    assetLabels = ["Property Values", "Savings Accounts", "Pensions Accounts", "Cars", "Other Assets"]
    liabilities = [valuation.mortgagesLiability, valuation.studentLoanLiability, valuation.personalLoanLiability,
                   valuation.carLoansLiability, valuation.otherDebtLiability]
    liabilitiesLabels = ["Mortgages", "Student Loans", "Personal Loans", "Car Loans", "Other Debt"]
    buildPieChart(assets, assetLabels, liabilities, liabilitiesLabels)

    print("finished building and saving charts")


def buildBarChart(dataframe):
    plt.figure(figsize=(24, 24))
    sns.set(style='darkgrid')
    barPlot = dataframe.plot(kind='bar', stacked=True)
    barPlot.set_xticklabels(["Assets", "Liabilities"])
    barPlot.legend(loc='upper right', bbox_to_anchor=(1, 1))
    plt.legend(fontsize='x-small')
    plt.xlabel('Assets & Liabilities')
    plt.ylabel('Value in £')
    plt.title("Personal Assets and Liabilities Breakdown by Bar Chart ")
    plt.savefig('static/images/personalBarChartValuation.jpg', bbox_inches='tight', dpi=300)
    plt.close()


def buildPieChart(assets, assetsLabels, liabilities, liabilitiesLabels):
    plt.figure(figsize=(7, 7))
    plt.pie(assets, labels=assetsLabels, colors=sns.color_palette('muted'), autopct='%.0f%%')
    plt.title("Personal Assets Breakdown by Pie Chart")
    plt.savefig('static/images/personalAssetPieChartValuation.jpg', bbox_inches='tight', dpi=300)
    plt.close()

    plt.figure(figsize=(7, 7))
    plt.pie(liabilities, labels=liabilitiesLabels, colors=sns.color_palette('muted'), autopct='%.0f%%')
    plt.title("Personal Liabilities Breakdown by Pie Chart")
    plt.savefig('static/images/personalLiabilitiesPieChartValuation.jpg', bbox_inches='tight', dpi=300)
    plt.close()

    plt.figure(figsize=(7, 7))
    totalAssetsAndLiabilities = [sum(assets), sum(liabilities)]
    plt.pie(totalAssetsAndLiabilities, labels=["Assets", "Liabilities"],
            colors=sns.color_palette('muted'), autopct='%.0f%%')
    plt.title("Total Personal Assets & Liabilities  Breakdown by Pie Chart")
    plt.savefig('static/images/totalAssetAndLiabilitiesPieChartValuation.jpg', bbox_inches='tight', dpi=300)
    plt.close()


def buildApiCharts(date_periods, closing_prices, stockName, fromDate, toDate):
    sns.set_style("darkgrid")
    sns.lineplot(date_periods, closing_prices)
    sns.set(rc={'figure.figsize': (40, 40)})
    plt.xticks(rotation=45)
    plt.xlabel('Date')
    plt.ylabel('Closing Price')
    plt.title(stockName + " Closing Prices from: " + fromDate + " to: " + toDate)
    plt.savefig('static/images/stockClosingPriceGraph.jpg', bbox_inches='tight', dpi=300)
    plt.close()
