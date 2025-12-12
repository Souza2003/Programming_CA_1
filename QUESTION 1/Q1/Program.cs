// QUESTION 1 (PART 1) (C#)

using System;
using System.Collections.Generic;

// Contact class
class Contact
{
    public string FirstName { get; set; }
    public string LastName { get; set; }
    public string Company { get; set; }
    public string Email { get; set; }
    public DateTime Birthdate { get; set; }
    
    private string mobileNumber;
    public string MobileNumber
    {
        get { return mobileNumber; }
        set
        {
            if (IsValidMobileNumber(value))
                mobileNumber = value;
            else
                throw new Exception("Invalid mobile number (must be 9 digits)");
        }
    }

    public Contact(string fName, string lName, string comp, string mobile, string mail, DateTime bday)
    {
        FirstName = fName;
        LastName = lName;
        Company = comp;
        MobileNumber = mobile;
        Email = mail;
        Birthdate = bday;
    }

    private bool IsValidMobileNumber(string value)
    {
        if (string.IsNullOrEmpty(value) || value.Length != 9)
            return false;
        
        long num;
        if (!long.TryParse(value, out num) || num <= 0)
            return false;
        
        return true;
    }

    // Method Overloading
    public void DisplayInfo()
    {
        Console.WriteLine("Name: " + FirstName + " " + LastName);
        Console.WriteLine("Company: " + Company);
        Console.WriteLine("Mobile: " + MobileNumber);
        Console.WriteLine("Email: " + Email);
        Console.WriteLine("Birthdate: " + Birthdate.ToString("dd/MM/yyyy"));
    }

    public void DisplayInfo(bool brief)
    {
        if (brief)
            Console.WriteLine(FirstName + " " + LastName + " - " + MobileNumber);
        else
            DisplayInfo();
    }
}

// ContactBook class
class ContactBook
{
    private List<Contact> contacts = new List<Contact>();

    public void AddContact(Contact contact)
    {
        contacts.Add(contact);
        Console.WriteLine("Contact added successfully!");
    }

    public void ShowAllContacts()
    {
        if (contacts.Count == 0)
        {
            Console.WriteLine("No contacts found.");
            return;
        }
        
        Console.WriteLine("\n--- All Contacts ---");
        for (int i = 0; i < contacts.Count; i++)
        {
            Console.Write((i + 1) + ". ");
            contacts[i].DisplayInfo(true);
        }
    }

    public void ShowContactDetails(int index)
    {
        if (index < 0 || index >= contacts.Count)
        {
            Console.WriteLine("Invalid contact number.");
            return;
        }
        
        Console.WriteLine("\n--- Contact Details ---");
        contacts[index].DisplayInfo();
    }

    public void UpdateContact(int index)
    {
        if (index < 0 || index >= contacts.Count)
        {
            Console.WriteLine("Invalid contact number.");
            return;
        }

        Contact c = contacts[index];
        Console.WriteLine("Leave blank to keep current value");

        c.FirstName = GetInput("First Name (" + c.FirstName + "): ", c.FirstName);
        c.LastName = GetInput("Last Name (" + c.LastName + "): ", c.LastName);
        c.Company = GetInput("Company (" + c.Company + "): ", c.Company);
        c.Email = GetInput("Email (" + c.Email + "): ", c.Email);

        Console.Write("Mobile Number (" + c.MobileNumber + "): ");
        string mobile = Console.ReadLine();
        if (!string.IsNullOrEmpty(mobile))
        {
            try
            {
                c.MobileNumber = mobile;
            }
            catch (Exception ex)
            {
                Console.WriteLine(ex.Message);
                return;
            }
        }

        Console.WriteLine("Contact updated successfully!");
    }

    public void DeleteContact(int index)
    {
        if (index < 0 || index >= contacts.Count)
        {
            Console.WriteLine("Invalid contact number.");
            return;
        }
        contacts.RemoveAt(index);
        Console.WriteLine("Contact deleted successfully!");
    }

    private string GetInput(string prompt, string current)
    {
        Console.Write(prompt);
        string input = Console.ReadLine();
        return string.IsNullOrEmpty(input) ? current : input;
    }
}

// Main Program
class Program
{
    static void Main(string[] args)
    {
        ContactBook book = new ContactBook();
        AddSampleContacts(book);

        bool exit = false;
        while (!exit)
        {
            Console.WriteLine("\n===== Contact Book System =====");
            Console.WriteLine("1. Add Contact");
            Console.WriteLine("2. Show All Contacts");
            Console.WriteLine("3. Show Contact Details");
            Console.WriteLine("4. Update Contact");
            Console.WriteLine("5. Delete Contact");
            Console.WriteLine("6. Exit");
            Console.Write("Choose an option: ");

            string choice = Console.ReadLine();

            switch (choice)
            {
                case "1":
                    AddNewContact(book);
                    break;
                case "2":
                    book.ShowAllContacts();
                    break;
                case "3":
                    Console.Write("Enter contact number: ");
                    int index3 = int.Parse(Console.ReadLine()) - 1;
                    book.ShowContactDetails(index3);
                    break;
                case "4":
                    Console.Write("Enter contact number to update: ");
                    int index4 = int.Parse(Console.ReadLine()) - 1;
                    book.UpdateContact(index4);
                    break;
                case "5":
                    Console.Write("Enter contact number to delete: ");
                    int index5 = int.Parse(Console.ReadLine()) - 1;
                    book.DeleteContact(index5);
                    break;
                case "6":
                    exit = true;
                    Console.WriteLine("Goodbye!");
                    break;
                default:
                    Console.WriteLine("Invalid option. Try again.");
                    break;
            }
        }
    }

    static void AddNewContact(ContactBook book)
    {
        try
        {
            Console.Write("First Name: ");
            string firstName = Console.ReadLine();
            Console.Write("Last Name: ");
            string lastName = Console.ReadLine();
            Console.Write("Company: ");
            string company = Console.ReadLine();
            Console.Write("Mobile Number (9 digits): ");
            string mobile = Console.ReadLine();
            Console.Write("Email: ");
            string email = Console.ReadLine();
            Console.Write("Birthdate (dd/mm/yyyy): ");
            DateTime birthdate = DateTime.Parse(Console.ReadLine());

            Contact newContact = new Contact(firstName, lastName, company, mobile, email, birthdate);
            book.AddContact(newContact);
        }
        catch (Exception ex)
        {
            Console.WriteLine("Error: " + ex.Message);
        }
    }

    static void AddSampleContacts(ContactBook book)
    {
        book.AddContact(new Contact("John", "Smith", "TechCorp", "123456789", "john@email.com", new DateTime(1990, 5, 15)));
        book.AddContact(new Contact("Mary", "Johnson", "WebSolutions", "234567890", "mary@email.com", new DateTime(1988, 3, 22)));
        book.AddContact(new Contact("James", "Williams", "DataSystems", "345678901", "james@email.com", new DateTime(1992, 7, 8)));
        book.AddContact(new Contact("Sarah", "Brown", "CloudTech", "456789012", "sarah@email.com", new DateTime(1985, 11, 30)));
        book.AddContact(new Contact("Michael", "Jones", "InfoSoft", "567890123", "michael@email.com", new DateTime(1991, 2, 14)));
        book.AddContact(new Contact("Emma", "Garcia", "NetWorks", "678901234", "emma@email.com", new DateTime(1993, 9, 5)));
        book.AddContact(new Contact("David", "Martinez", "AppDev", "789012345", "david@email.com", new DateTime(1987, 12, 19)));
        book.AddContact(new Contact("Lisa", "Rodriguez", "CodeFactory", "890123456", "lisa@email.com", new DateTime(1994, 4, 27)));
        book.AddContact(new Contact("Daniel", "Hernandez", "ByteInc", "901234567", "daniel@email.com", new DateTime(1989, 6, 11)));
        book.AddContact(new Contact("Jennifer", "Lopez", "DigitalPro", "112345678", "jennifer@email.com", new DateTime(1995, 1, 3)));
        book.AddContact(new Contact("Robert", "Wilson", "SysAdmin", "223456789", "robert@email.com", new DateTime(1986, 8, 25)));
        book.AddContact(new Contact("Linda", "Anderson", "DevHub", "334567890", "linda@email.com", new DateTime(1992, 10, 17)));
        book.AddContact(new Contact("William", "Thomas", "LogicSoft", "445678901", "william@email.com", new DateTime(1990, 3, 9)));
        book.AddContact(new Contact("Barbara", "Taylor", "SmartApps", "556789012", "barbara@email.com", new DateTime(1988, 7, 21)));
        book.AddContact(new Contact("Richard", "Moore", "TechVision", "667890123", "richard@email.com", new DateTime(1991, 11, 14)));
        book.AddContact(new Contact("Susan", "Jackson", "InnoTech", "778901234", "susan@email.com", new DateTime(1993, 5, 6)));
        book.AddContact(new Contact("Joseph", "Martin", "ProSystems", "889012345", "joseph@email.com", new DateTime(1987, 9, 28)));
        book.AddContact(new Contact("Jessica", "Lee", "FutureSoft", "990123456", "jessica@email.com", new DateTime(1994, 2, 12)));
        book.AddContact(new Contact("Thomas", "Perez", "GlobalTech", "111234567", "thomas@email.com", new DateTime(1989, 12, 4)));
        book.AddContact(new Contact("Karen", "White", "CoreSystems", "222345678", "karen@email.com", new DateTime(1995, 6, 18)));
    }
}