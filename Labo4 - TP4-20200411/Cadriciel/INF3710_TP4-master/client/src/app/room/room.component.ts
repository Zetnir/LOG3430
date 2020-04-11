import { Component, OnInit } from "@angular/core";
import { Room } from "../../../../common/tables/Room";
import { CommunicationService } from "../communication.service";

@Component({
  selector: "app-room",
  templateUrl: "./room.component.html",
  styleUrls: ["./room.component.css"]
})
export class RoomComponent implements OnInit {
  public constructor(private communicationService: CommunicationService) { }

  public hotelPKs: string[] = [];
  public duplicateError: boolean = false;
  public invalidHotelPK: boolean = false;
  public ngOnInit(): void {
      this.communicationService.getHotelPKs().subscribe((hotelPKs: string[]) => {
          this.hotelPKs = hotelPKs;
          console.log(this.duplicateError);
          console.log(this.hotelPKs);
      });
  }

  public validateHotelNo(hotelNo: string): void {
    this.invalidHotelPK = this.hotelPKs.indexOf(hotelNo) === -1;
    console.log("===" + hotelNo + this.invalidHotelPK)
  }

  public insertRoom( roomNo: string, hotelNo: string, typeRoom: string, price: number): void {
    const room: Room = {
        roomno: roomNo,
        hotelno: hotelNo,
        typeroom: typeRoom,
        price: price
    };
    this.communicationService.insertRoom(room).subscribe((res: number) => {
        console.log(res);
    });
}
}
