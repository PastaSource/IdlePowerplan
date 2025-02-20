import powerplan
         
def main():
    print("Enabling power saver plan")
    try:
        powerplan.change_current_scheme_to_powersaver()
    except Exception as e:
        print(f"Error changing powerplan: {e}")

if __name__ == "__main__":
    main()
