# Purdue-Big-Ten-Lineups
## An analysis of every basketball lineup used in Big Ten play by the Purdue Boilermakers. Data sourced from ESPN play by play. Game data was scraped, cleaned, transformed, and displayed using BeautifulSoup, Pandas, and Streamlit.

Interactive website can be found [here](https://purdue-big-ten-lineups.streamlit.app/)

Sample screenshots of the website:

<img width="949" alt="Website_1" src="https://github.com/d-fuqua/Purdue-Big-Ten-Lineups/assets/68402521/b8bbfac4-3605-486e-bd6b-7bdd76d1ce45">
 
<img width="945" alt="Website_2" src="https://github.com/d-fuqua/Purdue-Big-Ten-Lineups/assets/68402521/7cb61a11-0be7-47d4-9183-5410805f47e7">

## Summary of Insights
### Plus/Minus
- The Smith/Loyer/Morton/Furst/Edey lineup leads all lineups with a plus/minus of 56 in 227 minutes in all 20 games played. The Smith/Loyer/Morton/Gillis/Edey lineup had the second highest plus/minus of 53 in only 108 minutes in 17 games played. The Smith/Jenkins/Loyer/Gillis/Edey lineup had the third highest plus/minus of 22 in only 7 minutes, the highest plus/minus of any lineup with less than 10 minutes played.
- The Jenkins/Newman/Morton/Gillis/Edey lineup had the lowest plus/minus of all lineups with -12 in 8 minutes in 5 games played. The second lowest plus/minus was the Jenkins/Loyer/Newman/Gillis/Kaufman-Renn lineup with -8 in 21 minutes in 10 games played, which is also the the second highest minutes played of all lineups that have a negative plus/minus. Additionally, the Jenkins/Loyer/Newman/Furst/Edey lineups had the third lowest plus/minus with -5 in 9 minutes in 6 games played.

### Net Rating
- When analyzing Net Ratings, considering playing time of the lineup is essential due to Offensive Rating and Defensive Rating being a per 100 posessesions stat. So, if a lineup played few minutes, their Offensive and Defensive Ratings can be skewed.
- The top 3 lineups with the most amount of minutes with a _positive_ Net rating, the first lineup with the most minutes is the Smith/Loyer/Morton/Furst/Edey lineup with 227 minutes in 20 games with a Net Rating of 17.14. The second most minutes played is the Smith/Loyer/Morton/Gillis/Edey lineup with 108 minutes in 17 games with a Net Rating of 27.27. And, the Jenkins/Loyer/Morton/Furst/Edey lineup played 28 minutes in 9 games with a Net Rating of 9.09.
- For the top 3 lineups with the most amount of minutes with a _negative_ Net Rating, the lineup Smith/Loyer/Newman/Gillis/Edey had a Net Rating of -9.7 in 48 minutes in 9 games. The second most minutes played is the Jenkins/Loyer/Newman/Gillis/Kaufman-Renn lineup with 21 minutes in 10 games with a Net Rating of -29.57. Finally, the lineup with the third most minutes is the Smith/Jenkins/Newman/Gillis/Edey lineup with 19 minutes in 11 games with a Net Rating of -7.14.

### AST:TO
- Focusing on the previously mentioned lineups from the Plus/Minus and Net Rating sections allows us to examine AST:TO trends in lineups with high and low ratings.
- Of the mentioned top three lineups with the highest Plus/Minus, all had an AST:TO over 1 with the Smith/Jenkins/Loyer/Gillis/Edey lineup standing out with an AST:TO of 9.00.
- Meanwhile, the previous three lineups with the lowest Plus/Minus had an AST:TO less than 1, with the Jenkins/Newman/Morton/Gillis/Edey lineup recording 0.0, indicating no assists.
- Among the top three lineups with a _positive_ Net Rating, all featured an AST:TO greater than 1. Of these lineups, one hasn't been mentioned previously, the Jenkins/Loyer/Morton/Furst/Edey lineup, which had an AST:TO of 1.57.
- Of the top three lineups with a _negative_ Net Rating, two of the three have an AST:TO less than 1. Two of these lineups haven't been mentioned, with the Smith/Loyer/Newman/Gillis/Edey lineup had an AST:TO of 0.88 and the Smith/Jenkins/Newman/Gillis/Edey lineup had an AST:TO greater than 1, with a value of 1.50.

## Takeaways and Recommendations
- The Smith/Loyer/Morton/Furst/Edey lineup, along with the Smith/Loyer/Morton/Gillis/Edey lineup, were the most impactful due to their high Plus/Minus and Net Ratings. Their significant playing time likely contributed to their success and impact on Purdue's winning performance in the Big Ten regular season.
- Lineups with David Jenkins Jr. and Brandon Newman experienced challenges, particularly when Jenkins played as Point Guard and Newman as Small Forward. These lineups had weak Plus/Minus and AST:TO stats, indicating a need for improvement in those positions.
- For the upcoming season (2023-2024), the absence of Jenkins and Newman may provide an opportunity for new players to strengthen the backup Point Guard and Small Forward positions, potentially leading to better performance for lineups featuring bench players.
- The Smith/Loyer/Morton/Gillis/Edey lineup showed comparable results to the successful Smith/Loyer/Morton/Furst/Edey lineup but with only half the minutes played. Consider using Mason Gillis as the Power Forward with Zach Edey at Center, as Gillis' shooting abilities outperformed Caleb Furst, improving the lineup's overall performance.
