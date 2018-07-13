//
//  ViewController.swift
//  Drake
//
//  Created by Timothy Malaney on 7/12/18.
//  Copyright © 2018 Boats and Potreros. All rights reserved.
//

import UIKit

class ViewController: UIViewController, UIImagePickerControllerDelegate, UINavigationControllerDelegate {
    
    @IBOutlet weak var pickedImaged: UIImageView!
    
    @IBOutlet var captionLabel: UILabel!
    
    override func viewDidLoad() {
        super.viewDidLoad()
        UIApplication.shared.statusBarStyle = .lightContent
        // Do any additional setup after loading the view, typically from a nib.
    }

    override func didReceiveMemoryWarning() {
        super.didReceiveMemoryWarning()
        // Dispose of any resources that can be recreated.
    }

    
    @IBAction func camerabuttonaction(_ sender: UIButton) {
        if UIImagePickerController.isSourceTypeAvailable(UIImagePickerControllerSourceType.camera){
            let imagePicker = UIImagePickerController()
            imagePicker.delegate = self
            imagePicker.sourceType = UIImagePickerControllerSourceType.camera;
            imagePicker.allowsEditing = false
            self.present(imagePicker, animated: true, completion: nil)
        }
    }
    
    @IBAction func photolibraryaction(_ sender: UIButton) {
        if UIImagePickerController.isSourceTypeAvailable(UIImagePickerControllerSourceType.photoLibrary){
            let imagePicker = UIImagePickerController()
            imagePicker.delegate = self
            imagePicker.sourceType = UIImagePickerControllerSourceType.photoLibrary;
            imagePicker.allowsEditing = true
            self.present(imagePicker, animated: true, completion: nil)
        }
    }
    
    @IBAction func saveaction(_ sender: UIButton) {
        //        let requestData: Data
        //        do {
        //            requestData = try JSONSerialization.data(withJSONObject: dictionary, options: JSONSerialization.WritingOptions())
        //            request.httpBody = requestData
        //        }
        //        catch let error as NSError {
        //        }
        
        
        let imageData = UIImageJPEGRepresentation(pickedImaged.image!, 0.6)
        let compressedJPEGImage = UIImage(data: imageData!)
        let data = imageData!.base64EncodedString(options: Data.Base64EncodingOptions.lineLength64Characters)

        let url = URL(string: "http://17.236.37.73:5000")!
        var request = URLRequest(url: url)
        request.setValue("application/json", forHTTPHeaderField: "Content-Type")
        request.setValue("application/json", forHTTPHeaderField: "Accept-Language")
        request.httpMethod = "POST"
        //let postString: String = data
        let dictionary: [String:Any] = ["string": data]
        do {
            let requestData:Data = try JSONSerialization.data(withJSONObject: dictionary, options: JSONSerialization.WritingOptions())
            request.httpBody = requestData
        }
        catch let error as NSError {
        }
        let config = URLSessionConfiguration.default
        let session = URLSession(configuration: config)
        print("making call \(dictionary)")
        captionLabel.text = "Loading..."
        let task = session.dataTask(with: request) { (responseData, response, responseError) in
            DispatchQueue.main.async {
                var text: String = "I only love my bed and my momma I'm sorry"
                do {
                    if let object = try JSONSerialization.jsonObject(with: responseData!, options: []) as? [String: Any] {
                        print("responseData: \(object)")
                        text = object["caption"] as! String
                    }
                    self.captionLabel.text = text
                }
                catch {
                }
            }
        }
        task.resume()
        
        //let quotes: [String] = ["1", "2", "3", "4", "5", "6"]
    }
    
    func imagePickerController(_ picker: UIImagePickerController, didFinishPickingImage image: UIImage!, editingInfo: [NSObject : AnyObject]!){
        pickedImaged.image = image
        self.dismiss(animated: true, completion: nil);
    }
    
}
