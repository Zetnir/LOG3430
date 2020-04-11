import { Component } from "@angular/core";
import { CommunicationService } from "./../communication.service";

@Component({
  selector: "app-hotel",
  templateUrl: "./hotel.component.html",
  styleUrls: ["./hotel.component.css"]
})

export class HotelComponent {

  public constructor(private communicationService: CommunicationService) { }


  public duplicateError: boolean = false;

  public insertHotel(hotelNo: string, hotelName: string, hotelCity: string): void {
    const hotel: any = {
        "hotelNo" : hotelNo,
        "hotelName" : hotelName,
        "city" : hotelCity
    };
    this.communicationService.insertHotel(hotel).subscribe((res: number) => {
        if (res > 0) {
            this.communicationService.filter("update");
        }
        this.duplicateError = (res === -1);
    });
  }
}
