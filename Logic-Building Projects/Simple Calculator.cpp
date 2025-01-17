#include <iostream>
using namespace std;

void displayMenu() {
    cout << "Simple Calculator" << endl;
    cout << "-----------------" << endl;
    cout << "1. Addition (+)" << endl;
    cout << "2. Subtraction (-)" << endl;
    cout << "3. Multiplication (*)" << endl;
    cout << "4. Division (/)" << endl;
    cout << "5. Exit" << endl;
    cout << "-----------------" << endl;
    cout << "Enter your choice: ";
}

int main() {
    int choice;
    double num1, num2, result;

    do {
        displayMenu();
        cin >> choice;

        if (choice >= 1 && choice <= 4) {
            cout << "Enter first number: ";
            cin >> num1;
            cout << "Enter second number: ";
            cin >> num2;
        }

        switch (choice) {
            case 1:
                result = num1 + num2;
            cout << "Result: " << num1 << " + " << num2 << " = " << result << endl;
            break;

            case 2:
                result = num1 - num2;
            cout << "Result: " << num1 << " - " << num2 << " = " << result << endl;
            break;

            case 3:
                result = num1 * num2;
            cout << "Result: " << num1 << " * " << num2 << " = " << result << endl;
            break;

            case 4:
                if (num2 != 0) {
                    result = num1 / num2;
                    cout << "Result: " << num1 << " / " << num2 << " = " << result << endl;
                } else {
                    cout << "Error: Division by zero is not allowed." << endl;
                }
            break;

            case 5:
                cout << "Exiting the calculator. Goodbye!!" << endl;
            break;

            default:
                cout << "Invalid choice. Please try again." << endl;
            break;
        }

        cout << endl;

    } while (choice != 5);

    return 0;
}
