"use client";
import { useEffect, useState } from "react";
import "../styles/Hero.css";
import Tiles from "./Tiles"

export default function Hero() {
    const [isHovered, setIsHovered] = useState<boolean>(false);
    const handleMouseEnter = (event: React.MouseEvent<HTMLVideoElement>) => {
        event.currentTarget.play();
        setIsHovered(true);
    };

    const handleMouseLeave = (event: React.MouseEvent<HTMLVideoElement>) => {
        event.currentTarget.pause();
    };

    return (
        <div className="flex flex-col items-center justify-center min-h-screen">

            <div id="container">
                <Tiles />
                <h1 className="Heading">
                    {/* <span className="C">C</span>
                    <span className="U">U</span>
                    <span className="R">R</span>
                    <span className="A">A</span>
                    <span className="T">T</span>
                    <span className="H">H</span>
                    <span className="O">O</span>
                    <span className="R">R</span> */}
                    <span className="N">CURATHOR</span>
                </h1>
            </div>
            <style jsx>{`
                .video, .book, .video1, .vid4 {
                    transition: filter 0.5s ease;
                    filter: grayscale(100%);
                }
                    
                .video:hover, .book:hover, .video1:hover, .vid4:hover {
                    filter: grayscale(0%);
                }
            `}</style>
            <video
                className="video1"
                src={`https://raipur.s3.ap-south-1.amazonaws.com/vid1.mp4`}
                onMouseEnter={handleMouseEnter}
                onMouseLeave={handleMouseLeave}
                loop
            />
            <video
                className="video"
                src={`https://raipur.s3.ap-south-1.amazonaws.com/vid2.mp4`}
                onMouseEnter={handleMouseEnter}
                onMouseLeave={handleMouseLeave}
                loop
            />
            <video
                className="book"
                src={`https://raipur.s3.ap-south-1.amazonaws.com/vid3.mp4`}
                onMouseEnter={handleMouseEnter}
                onMouseLeave={handleMouseLeave}
                loop
            />
            <video
                className="vid4"
                src={`https://cdn.rauno.me/flume-s2.mp4#t=0.01`}
                onMouseEnter={handleMouseEnter}
                onMouseLeave={handleMouseLeave}
                loop
            />

        </div>
    );
}