import requests

def verify_recaptcha(token):
    print("hi")
    secret_key = "6LcXxroqAAAAAGeX9BkQ5oAxyKeeyoGPpesYUQkL"  # Your secret key from Google reCAPTCHA admin console
    url = "https://www.google.com/recaptcha/api/siteverify"
    payload = {"secret": secret_key, "response": token}

    # Send the token to Google's API
    response = requests.post(url, data=payload)
    result = response.json()

    print("Recaptcha response: " + str(result))

    # Process the verification result
    if result.get("success"):
        print("CAPTCHA verified successfully!")
        return str(result)
    else:
        print("CAPTCHA verification failed.")
        return str(result)



#verify_recaptcha("03AFcWeA7WYMlQjcSdty2Ej3NTHuSJcvJT-J7hq0t-AdK4BwWcuxmf7MH0_ANQytGYFoXiWAmxjFoGgZv36JQUTkwd_n_YJfEucLiBN6lEFz7JJ3jkwgnNMe6PCEBLvTU51SsdNpvMg9_br7FCsK7FcI_Ns_XrEd0xqxYie4NCeuRrldIJPlD9JkvX3mj42veOmodp7S2_j9kQ63s162Y-2SGg8baCVa-khwVNp8LTo9wQ76YsRKQxyFHVWQwT_d4P-DbF1LhHC99ZjEn_JmDS374wBppwVBF1W-fNtKenE_A7y4zCgCP4LOy0209rHMAKWAVlzq5EBvjr44J75HNf07VOIF4z0NWUUm_ttEDipFb3fyDCPpOEDlWMAzsI9xWRGdo3xM7Eshf5SvAWVuLO8-LOThY3gM9SEx9zw5NJkT5A89E0RwoclMgi1hLT2qGH5cm4OAxK8Svj_wdYCG-1ksco1si6029Lu6r7kbefn5ZsHJcsSNc38RtWr2T4tsV8rFTPwiBatp7DGDsIHFNz8Fgs5V2Fthx9tj07JJKlM_km3wZH-VcVZN1kFdBGHozpzm3F55xlWv_-SftvSu6XnHRFnIJf86OXbzZRPaz7HRzKNOjzNhi9RMHwhyrO4bvnYSoawxtkOjdNfUeTz_GbV41ECRbSXNf5AGBWYfa-yw_Rq1fKA03jed7vESfP6u1K3VRCka8eQggiWcfeggEsNDBmJp2BNO1891GeFUHrIv9QiSuvDmIhEBfoPKVU2Op3c95mAmeJaZYtPU20K6v7tYQGm1FxGVVLrZUnwRsKi6SaJouIB7j-UGO-VUcuHDNn9gcefUBwaY6rQbKkzVM2SLj4TA1nJW2s1BM0OoNBe1ZZ76KEq-exFGHcOgNilWIc2XzEAO4aymTjZIzfDZmXOU2rYAIQTcr5ORiuoLNXVeU3_RbX5tlyxtuRuyowy7LTqcnUer8vk5GvLwQviRJiIS5iH9cDaqESTlRnhqcoJQXswz5EQurMBC7K7sl_qQS_AKuzD4kVgWFOgQL2vCJiXLzQ-QmUou1ncA08QjcVmN02cjA60F0nkiJfIcq6MJIefCv180RQOMWRJL9DX9gWtokLFUgalqfkCWg9g0hGjy4G7s7qGoSzmA78jlSP1J6pE0St7ddd2k1-2eDoEsLhu9kJxZvcuCsJvcQ0tLIRMHGKtp9D13wqosSwuT4c3KUsG_PfB3NgFRSauzYhGXQJs8dQyavsXpBP3_3ThppDwBoXeFTOMAnpTUFyX3s5QeMiJ-m1ajBQZTwTSBtnhaQdpf5rqqMvliKASj61xjRxwS07-tNfoQdlIHiE1hSq9YHnd33C9Q5_QFIDQqN0hmWFyEUb8-rrWlJ6qbqSx6E780e2XPFr3STGeo75PFgqFY0Fh4lcK0m9u9FIWorFI2fx3X2eiFwFvtQhknvbMeyOQytF4Kbbsbw7G4jCoemrWoqJD6W-jPRH6bNP5tc_DKj0LcIb-ug-inT1oSbn5jR-iQbzqcGgCLG4NZgB9ij1sJb8Pqm2mVVFJuKWOiGxU1-qnbza3fuDROrAtEE3TH6zRz2lUGW8degOnB7EZK9z4ukgDsbT5OxsG5kwnynuYGgr5D-vC6khg9jDgvQpUdGdOrhPJi19UufRTkNv-G5ZkpnAM1gUajDxSXYa4kzuaz06WvCeuidmUaMHXvsng1spgHbxD4GTY1gUp7u98WK5Rswxd6fM6z-0UmjEhdUA-NZ9ZS_m8_9kWkGVeGwU8g2OfVhkvRByn8ecKPYTPkVgHK-UD8zvvL4lwbKSUVIau4D5mT3GXsbZGKhYw1sKOwSo2xPlRTNoDbeY2S3foR380DfZiwy9x2CbmbR4pRD6zD4buEKD3Wx4guJy8D0yCKMHAv7-WMKSvWNM_PEDkxyb9qTzUEiFOBBmMw68y9XIu23SvqofH8WRS-2hCLz1x9eu_14z8B16sHUM56mE0b0cD_ng0cUDVp22VZ7O")