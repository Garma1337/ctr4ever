import {Link} from "@mui/material";

const IndexView = () => {
    return (
        <>
            Welcome!
            <br/><br/>
            This is the new ctr4ever website. The <Link href="http://ctr4ever.joora.fr/home.php">other page</Link> is
            quite outdated and I think we all agree it was due an
            overhaul. The new website
            uses latest technology and also sports a range of new features. I will not go into detail of everything, but
            to name a few things:
            <ul>
                <li>
                    The new website is available via HTTPS, is responsive and supports light and dark mode
                </li>
                <li>
                    Players can register without having to DM someone on Discord with their credentials (<i>how is this
                    considered a feature???</i>)
                </li>
                <li>
                    Submissions now contain information about the ruleset and the platform they were made on - currently
                    there are 3 rulesets (Unrestricted, Classic and Skipless) and 2 platforms (Console and Emulator)
                </li>
                <li>
                    All leaderboards are now always filterable by category, engine, game version, ruleset and platform
                    (this means there are no more "Course (Fast Character)" categories and WRs are simply the fastest
                    times for your selected set of filters)
                </li>
                <li>
                    A history of submissions is kept for every player - leaderboards will still only show the fastest
                    time of a player for the selected set of filters
                </li>
            </ul>
            There is a load of other small improvements that naturally come with the more modern interface (such as the
            ability to see a submission comment without having to hover over the entry ...) but I'm not listing all of
            those here.
            <br/><br/>
            Explore the new website to your heart's content.
            <br/><br/>
            - Garma
        </>
    );
}

export default IndexView;