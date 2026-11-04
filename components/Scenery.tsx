export default function Scenery({
  type = "all",
  className = "",
}: {
  type?: string;
  className?: string;
}) {
  return (
    <svg
      className={className}
      viewBox="0 0 1000 510"
      role="img"
      aria-label={
        type === "forest"
          ? "Pulau hutan ajaib"
          : type === "town"
            ? "Kota percakapan"
            : type === "castle"
              ? "Kastil pengetahuan"
              : "Peta pulau petualangan dengan hutan, kota, dan kastil"
      }
    >
      <defs>
        <linearGradient id={`water-${type}`} x2="0" y2="1">
          <stop stopColor="#9edff5" />
          <stop offset="1" stopColor="#d3f0f6" />
        </linearGradient>
        <linearGradient id={`land-${type}`} x2="0" y2="1">
          <stop stopColor="#c6e8a4" />
          <stop offset="1" stopColor="#91c985" />
        </linearGradient>
        <filter id={`shadow-${type}`} x="-20%" width="140%" height="140%">
          <feDropShadow
            dx="0"
            dy="12"
            stdDeviation="5"
            floodColor="#447b83"
            floodOpacity=".16"
          />
        </filter>
      </defs>
      <rect width="1000" height="510" rx="40" fill={`url(#water-${type})`} />
      <g fill="white" opacity=".8">
        <ellipse cx="118" cy="82" rx="68" ry="18" />
        <circle cx="109" cy="66" r="25" />
        <circle cx="145" cy="71" r="19" />
        <ellipse cx="818" cy="62" rx="60" ry="16" />
        <circle cx="798" cy="49" r="24" />
        <circle cx="831" cy="51" r="17" />
      </g>
      <g stroke="white" strokeWidth="4" strokeLinecap="round" opacity=".7">
        <path d="M50 340h55m-25 22h58M814 397h92m-42 22h55M395 475h115" />
      </g>
      <ellipse
        cx="506"
        cy="384"
        rx="403"
        ry="70"
        fill="#62b7c7"
        opacity=".16"
      />
      <path
        d="M107 318Q78 252 195 220Q199 175 290 176Q344 108 449 153Q522 112 590 157Q706 128 743 187Q859 197 866 265Q951 324 855 366Q810 410 688 398Q568 452 470 413Q365 431 283 391Q151 408 107 318Z"
        fill="#e7cf93"
      />
      <path
        d="M113 293Q92 238 202 208Q236 164 301 173Q356 114 449 151Q534 111 594 158Q709 130 747 192Q859 196 865 262Q912 317 837 347Q783 390 688 376Q572 426 472 391Q368 408 286 371Q169 389 113 293Z"
        fill={`url(#land-${type})`}
        filter={`url(#shadow-${type})`}
      />
      <path
        d="M257 279Q355 246 405 299T563 302Q640 267 756 291"
        fill="none"
        stroke="#fcf1ca"
        strokeWidth="30"
        strokeLinecap="round"
      />
      <path
        d="M257 279Q355 246 405 299T563 302Q640 267 756 291"
        fill="none"
        stroke="#d2b987"
        strokeWidth="3"
        strokeDasharray="3 15"
        strokeLinecap="round"
      />
      {(type === "all" || type === "forest") && (
        <g>
          <path d="M190 232 247 107 307 231Z" fill="#83b9a1" />
          <path d="m246 107-18 43h40Z" fill="#edf7d9" />
          <path d="M145 279 180 197 214 279Z" fill="#519b72" />
          {[
            [190, 227],
            [235, 252],
            [305, 200],
            [333, 243],
            [155, 293],
            [292, 285],
          ].map(([x, y], i) => (
            <g key={i}>
              <rect
                x={x - 5}
                y={y - 20}
                width="10"
                height="52"
                rx="4"
                fill="#937653"
              />
              <ellipse
                cx={x}
                cy={y - 24}
                rx="30"
                ry="38"
                fill={i % 2 ? "#45986f" : "#60b57b"}
              />
              <ellipse cx={x - 8} cy={y - 34} rx="16" ry="21" fill="#8dce8b" />
            </g>
          ))}
          <path d="M219 288q33-48 68 0v34h-68Z" fill="#b18c61" />
          <path d="M233 289q20-30 40 0v33h-40Z" fill="#546f53" />
          <circle cx="279" cy="295" r="5" fill="#FFD95A" />
        </g>
      )}
      {(type === "all" || type === "town") && (
        <g>
          <g transform="translate(411 177)">
            <rect width="64" height="87" rx="5" fill="#ffe9a8" />
            <path d="m-12 5 43-41L77 5Z" fill="#e48665" />
            <rect x="24" y="47" width="20" height="40" rx="10" fill="#a58162" />
            <rect x="9" y="18" width="14" height="19" rx="5" fill="#85cad6" />
            <rect x="41" y="18" width="14" height="19" rx="5" fill="#85cad6" />
          </g>
          <g transform="translate(500 198)">
            <rect width="78" height="69" rx="5" fill="#fdf4d6" />
            <path d="M-8 6 39-28 86 6Z" fill="#e1a252" />
            <rect x="28" y="35" width="23" height="34" rx="5" fill="#b8906d" />
            <path d="M-3 13h84v17H-3Z" fill="#ff9066" />
            <path
              d="M9 13v17m20-17v17m20-17v17m20-17v17"
              stroke="#fff3d6"
              strokeWidth="10"
            />
          </g>
          <g transform="translate(470 135)">
            <rect width="28" height="66" rx="3" fill="#fff3d4" />
            <path d="m-5 1 19-23L34 1Z" fill="#e48665" />
            <circle
              cx="14"
              cy="22"
              r="9"
              fill="#ffdb6c"
              stroke="#ba8d5e"
              strokeWidth="2"
            />
            <path d="M14 17v6h5" stroke="#675b57" strokeWidth="2" fill="none" />
          </g>
          <ellipse cx="483" cy="311" rx="29" ry="11" fill="#72b7be" />
          <ellipse cx="483" cy="307" rx="25" ry="8" fill="#bbeaf0" />
          <path d="M483 307v-27" stroke="#fff3d6" strokeWidth="8" />
          <path
            d="M467 282q16-15 32 0"
            stroke="#fff3d6"
            strokeWidth="5"
            fill="none"
          />
        </g>
      )}
      {(type === "all" || type === "castle") && (
        <g transform="translate(663 117)">
          <path d="m-22 104 58-80 80 105Z" fill="#a8afca" />
          <rect x="7" y="52" width="105" height="102" rx="5" fill="#eae4f5" />
          <rect x="-8" y="35" width="35" height="127" rx="5" fill="#d8cdec" />
          <rect x="88" y="35" width="35" height="127" rx="5" fill="#d8cdec" />
          <path d="m-17 38 26-42 27 42Zm96 0 26-42 27 42Z" fill="#9786c5" />
          <rect x="41" y="9" width="34" height="79" fill="#eae4f5" />
          <path d="m32 12 26-43 26 43Z" fill="#ad98d4" />
          <path
            d="M58-31v-29l31 9-31 11"
            fill="#ffcf64"
            stroke="#bc9857"
            strokeWidth="2"
          />
          <path d="M41 154v-35a18 18 0 0 1 36 0v35" fill="#8e84b4" />
          <path
            d="M9 76v18m96-18v18M58 41v15"
            stroke="#849bbe"
            strokeWidth="12"
            strokeLinecap="round"
          />
          <path d="M28 166h63l15 15H13Z" fill="#c5b8da" />
        </g>
      )}
      <g fill="#fff9d7">
        <circle cx="356" cy="350" r="4" />
        <circle cx="622" cy="335" r="5" />
        <circle cx="800" cy="282" r="4" />
      </g>
      <g fill="#efac8e">
        <circle cx="345" cy="337" r="5" />
        <circle cx="611" cy="348" r="4" />
        <circle cx="809" cy="299" r="5" />
      </g>
      <g transform="translate(96 407) rotate(-14)">
        <circle r="36" fill="#ffedba" stroke="#d3b97a" strokeWidth="4" />
        <path d="m0-28 9 26-9 21-9-21Z" fill="#e98a68" />
        <path d="m0 21 9-23H-9Z" fill="#6e9caa" />
        <circle r="4" fill="#fff5dc" />
      </g>
      <g transform="translate(841 386)">
        <path d="m0 5 29-11 30 11v28H0Z" fill="#ae7f52" />
        <path d="M0 5q30-24 59 0v9H0Z" fill="#c7985e" />
        <path d="M14 1v33m30-33v33" stroke="#f3d183" strokeWidth="6" />
        <rect x="24" y="12" width="12" height="12" rx="3" fill="#ffda69" />
      </g>
    </svg>
  );
}
