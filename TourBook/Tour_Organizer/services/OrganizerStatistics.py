

class OrganizerStatistics:

    def get_tour_statistics(self, tours):
        """
        Get tour statistics such as tours per month and profits per month.

        Args:
            tours (QuerySet): A queryset of tours.

        Returns:
            list: A list of dictionaries containing month-wise tour statistics.
        """
        months = self._initialize_monthly_data()
        total_profit = self._calculate_total_profit(tours)
        tours_per_month, profits_per_month = self._populate_monthly_statistics(
            tours, months)
        result = self._compile_final_result(
            months, tours_per_month, profits_per_month, total_profit)

        return result

    def _initialize_monthly_data(self):
        """
        Initializes dictionaries for counting tours and profits per month.

        Returns:
            list, dict, dict: List of month names, and initialized dictionaries for tours and profits.
        """
        months = ["January", "February", "March", "April", "May", "June",
                  "July", "August", "September", "October", "November", "December"]
        return months

    def _calculate_total_profit(self, tours):
        """
        Calculate the total profit from all tours.

        Args:
            tours (QuerySet): A queryset of tours.

        Returns:
            float: The total profit.
        """
        return sum(tour.seat_num * tour.seat_cost for tour in tours)

    def _populate_monthly_statistics(self, tours, months):
        """
        Populates the tours and profits data per month.

        Args:
            tours (QuerySet): A queryset of tours.
            months (list): List of month names.

        Returns:
            dict, dict: Dictionaries containing tours and profits per month.
        """
        tours_per_month = {month: 0 for month in months}
        profits_per_month = {month: 0 for month in months}

        for tour in tours:
            month_name = tour.start_date.strftime("%B")
            tours_per_month[month_name] += 1
            profits_per_month[month_name] += tour.seat_num * tour.seat_cost

        return tours_per_month, profits_per_month

    def _calculate_profit_percentage(self, profits_per_month, total_profit):
        """
        Calculates the profit percentage for each month.

        Args:
            profits_per_month (dict): Profits per month.
            total_profit (float): Total profit from all tours.

        Returns:
            dict: Profits per month as a percentage of the total profit.
        """
        if total_profit > 0:
            return {month: round(profit / total_profit * 100, 2) for month, profit in profits_per_month.items()}
        return {month: 0 for month in profits_per_month}

    def _compile_final_result(self, months, tours_per_month, profits_per_month, total_profit):
        """
        Compiles the final result into a list of dictionaries.

        Args:
            months (list): List of month names.
            tours_per_month (dict): Dictionary containing tours per month.
            profits_per_month (dict): Dictionary containing profits per month.
            total_profit (float): Total profit from all tours.

        Returns:
            list: A list of dictionaries with month-wise tour statistics.
        """
        result = []
        profits_percentage = self._calculate_profit_percentage(
            profits_per_month, total_profit)

        for month in months:
            data = {
                "month": month,
                "count": tours_per_month[month],
                "profits_per_month": f"{profits_percentage[month]}%"
            }
            result.append(data)

        return result
